"""Audits GCP connection and effective access capabilities.

This script checks:
- Connection health with Google Cloud APIs.
- Project hierarchy visibility.
- IAM policy visibility.
- Effective permissions related to bucket/object operations.

It also exports TXT reports automatically in PT-BR and EN.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any

import google.auth
from google.auth.transport.requests import AuthorizedSession
from google.cloud import storage
import yaml


def setup_logging() -> logging.Logger:
    """Configures friendly terminal logging.

    Returns:
        Configured logger instance.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    return logging.getLogger("gcp_access_audit")


@dataclass(frozen=True)
class AuditConfig:
    """Holds configuration for the GCP access audit.

    Attributes:
        language: Report language. Accepted values: "pt-BR" or "en".
        project_id: GCP project ID to inspect.
        bucket_name_for_checks: Existing bucket used to validate metadata access.
        test_permissions: IAM permissions to evaluate via testIamPermissions.
    """

    language: str
    project_id: str
    bucket_name_for_checks: str
    test_permissions: list[str]


class Localization:
    """Loads localized labels and value tokens from YAML files."""

    def __init__(self, base_dir: Path, language: str) -> None:
        """Initializes localization resources.

        Args:
            base_dir: Directory containing language YAML files.
            language: Language code from config.

        Raises:
            ValueError: If language is unsupported.
        """
        message_file = (
            base_dir / "messages_pt-BR.yaml"
            if language == "pt-BR"
            else base_dir / "messages_en.yaml"
            if language == "en"
            else None
        )
        if message_file is None:
            raise ValueError("Unsupported language. Use 'pt-BR' or 'en'.")

        self.language = language
        self.messages = self._load_yaml(message_file)

    def label(self, key: str) -> str:
        """Returns a localized label key."""
        return str(self.messages["labels"][key])

    def value(self, key: str) -> str:
        """Returns a localized value token."""
        return str(self.messages["values"][key])

    def level(self, key: str) -> str:
        """Returns a localized access level label."""
        return str(self.messages["levels"][key])

    def capability_name(self, key: str) -> str:
        """Returns a localized capability display name."""
        return str(self.messages["capability_names"][key])

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        """Loads a YAML file into a dictionary."""
        with path.open("r", encoding="utf-8") as file:
            loaded = yaml.safe_load(file) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"Invalid YAML structure in: {path}")
        return loaded


class GCPAccessAuditor:
    """Performs connection and access checks against GCP APIs."""

    def __init__(self, config: AuditConfig) -> None:
        """Initializes auth/session clients for auditing."""
        self.config = config
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", config.project_id)
        credentials, detected_project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.credentials = credentials
        self.detected_project = detected_project
        self.session = AuthorizedSession(credentials)
        self.storage_client = storage.Client(project=config.project_id, credentials=credentials)

    def run(self, i18n: Localization) -> dict[str, Any]:
        """Executes the full audit and builds a localized report."""
        connection = self._check_connection(i18n)
        hierarchy = self._check_hierarchy(i18n)
        iam = self._check_iam_visibility(i18n)
        permissions_result = self._check_permissions(i18n)
        bucket_metadata = self._check_bucket_metadata_access(i18n)
        storage_bucket_permissions = self._check_storage_bucket_permissions(i18n)

        capabilities = self._build_capabilities(
            i18n,
            permissions_result,
            bucket_metadata,
            storage_bucket_permissions,
        )
        level = self._infer_access_level(i18n, permissions_result)
        recommendations = self._build_recommendations(i18n, permissions_result)

        return {
            i18n.label("report_title"): {
                i18n.label("connection"): connection,
                i18n.label("hierarchy"): hierarchy,
                i18n.label("iam"): iam,
                i18n.label("permissions"): permissions_result,
                "storage_bucket_permissions": storage_bucket_permissions,
                i18n.label("capabilities"): capabilities,
                i18n.label("access_level"): level,
                i18n.label("recommended_actions"): recommendations,
            }
        }

    @staticmethod
    def _is_service_disabled_error(error_text: str) -> bool:
        """Checks whether an API error represents SERVICE_DISABLED."""
        upper_text = error_text.upper()
        return "SERVICE_DISABLED" in upper_text or "HAS NOT BEEN USED IN PROJECT" in upper_text

    def _check_connection(self, i18n: Localization) -> dict[str, Any]:
        """Checks token/session and storage API connectivity."""
        try:
            self.storage_client.list_buckets(project=self.config.project_id, max_results=1)
            return {
                "status": i18n.value("ok"),
                "project_from_config": self.config.project_id,
                "project_from_credentials": self.detected_project,
            }
        except Exception as error:
            return {
                "status": i18n.value("failed"),
                "project_from_config": self.config.project_id,
                "project_from_credentials": self.detected_project,
                "error": str(error),
            }

    def _check_hierarchy(self, i18n: Localization) -> dict[str, Any]:
        """Reads project metadata (including parent hierarchy when available)."""
        url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{self.config.project_id}"
        response = self.session.get(url)
        if response.status_code != 200:
            return {
                "status": i18n.value("failed"),
                "http_status": response.status_code,
                "error": response.text,
            }

        payload = response.json()
        parent = payload.get("parent") or {}
        return {
            "status": i18n.value("ok"),
            "project_id": payload.get("projectId"),
            "project_number": payload.get("projectNumber"),
            "lifecycle_state": payload.get("lifecycleState"),
            "parent_type": parent.get("type"),
            "parent_id": parent.get("id"),
        }

    def _check_iam_visibility(self, i18n: Localization) -> dict[str, Any]:
        """Checks if current identity can read project IAM policy."""
        url = (
            f"https://cloudresourcemanager.googleapis.com/v1/projects/{self.config.project_id}:getIamPolicy"
        )
        response = self.session.post(url, json={})
        if response.status_code != 200:
            return {
                "status": i18n.value("failed"),
                "http_status": response.status_code,
                "can_read_iam_policy": False,
                "error": response.text,
            }

        payload = response.json()
        bindings = payload.get("bindings", [])
        return {
            "status": i18n.value("ok"),
            "can_read_iam_policy": True,
            "binding_count": len(bindings),
            "etag_present": bool(payload.get("etag")),
        }

    def _check_permissions(self, i18n: Localization) -> dict[str, Any]:
        """Evaluates effective permissions using projects:testIamPermissions."""
        url = (
            f"https://cloudresourcemanager.googleapis.com/v1/projects/{self.config.project_id}:testIamPermissions"
        )
        response = self.session.post(url, json={"permissions": self.config.test_permissions})

        if response.status_code != 200:
            error_text = response.text
            service_disabled = self._is_service_disabled_error(error_text)
            return {
                "status": i18n.value("failed"),
                "http_status": response.status_code,
                "granted_permissions": [],
                "missing_permissions": self.config.test_permissions,
                "error": error_text,
                "verified": False,
                "not_verified_reason": (
                    "resource_manager_api_disabled" if service_disabled else "api_error"
                ),
            }

        payload = response.json()
        granted = payload.get("permissions", [])
        granted_set = set(granted)
        missing = [perm for perm in self.config.test_permissions if perm not in granted_set]

        return {
            "status": i18n.value("ok"),
            "granted_permissions": granted,
            "missing_permissions": missing,
            "verified": True,
            "not_verified_reason": None,
        }

    def _check_storage_bucket_permissions(self, i18n: Localization) -> dict[str, Any]:
        """Checks bucket-level Storage permissions directly via Storage API.

        Returns:
            Dictionary with direct bucket permission checks.
        """
        try:
            bucket = self.storage_client.lookup_bucket(self.config.bucket_name_for_checks)
            if bucket is None:
                return {
                    "status": i18n.value("failed"),
                    "verified": False,
                    "granted_permissions": [],
                    "requested_permissions": [
                        "storage.buckets.get",
                        "storage.buckets.delete",
                        "storage.objects.create",
                        "storage.objects.delete",
                        "storage.objects.get",
                    ],
                    "not_verified_reason": "bucket_not_visible",
                }

            requested_permissions = [
                "storage.buckets.get",
                "storage.buckets.delete",
                "storage.objects.create",
                "storage.objects.delete",
                "storage.objects.get",
            ]
            granted = bucket.test_iam_permissions(requested_permissions)
            return {
                "status": i18n.value("ok"),
                "verified": True,
                "requested_permissions": requested_permissions,
                "granted_permissions": granted,
                "not_verified_reason": None,
            }
        except Exception as error:
            return {
                "status": i18n.value("failed"),
                "verified": False,
                "granted_permissions": [],
                "requested_permissions": [
                    "storage.buckets.get",
                    "storage.buckets.delete",
                    "storage.objects.create",
                    "storage.objects.delete",
                    "storage.objects.get",
                ],
                "not_verified_reason": "storage_api_error",
                "error": str(error),
            }

    def _check_bucket_metadata_access(self, i18n: Localization) -> dict[str, Any]:
        """Checks whether configured bucket metadata is readable."""
        try:
            bucket = self.storage_client.lookup_bucket(self.config.bucket_name_for_checks)
            if bucket is None:
                return {
                    "status": i18n.value("failed"),
                    "can_read_bucket_metadata": False,
                    "bucket_exists_or_visible": False,
                }

            return {
                "status": i18n.value("ok"),
                "can_read_bucket_metadata": True,
                "bucket_exists_or_visible": True,
                "bucket_location": bucket.location,
            }
        except Exception as error:
            return {
                "status": i18n.value("failed"),
                "can_read_bucket_metadata": False,
                "bucket_exists_or_visible": False,
                "error": str(error),
            }

    def _build_capabilities(
        self,
        i18n: Localization,
        permissions_result: dict[str, Any],
        bucket_metadata: dict[str, Any],
        storage_bucket_permissions: dict[str, Any],
    ) -> dict[str, str]:
        """Builds localized capability map based on permission checks."""
        project_granted = set(permissions_result.get("granted_permissions", []))
        bucket_granted = set(storage_bucket_permissions.get("granted_permissions", []))

        project_verified = bool(permissions_result.get("verified"))
        bucket_verified = bool(storage_bucket_permissions.get("verified"))

        def resolve(permission: str, verified: bool, granted_set: set[str]) -> str:
            if not verified:
                return i18n.value("not_verified")
            return i18n.value("allowed") if permission in granted_set else i18n.value("denied")

        capability_map: dict[str, str] = {}

        capability_map[i18n.capability_name("create_bucket")] = resolve(
            "storage.buckets.create",
            project_verified,
            project_granted,
        )
        capability_map[i18n.capability_name("delete_bucket")] = resolve(
            "storage.buckets.delete",
            bucket_verified,
            bucket_granted,
        )
        capability_map[i18n.capability_name("upload_object")] = resolve(
            "storage.objects.create",
            bucket_verified,
            bucket_granted,
        )
        capability_map[i18n.capability_name("delete_object")] = resolve(
            "storage.objects.delete",
            bucket_verified,
            bucket_granted,
        )
        capability_map[i18n.capability_name("read_object")] = resolve(
            "storage.objects.get",
            bucket_verified,
            bucket_granted,
        )
        capability_map[i18n.capability_name("read_project")] = resolve(
            "resourcemanager.projects.get",
            project_verified,
            project_granted,
        )
        capability_map[i18n.capability_name("read_iam_policy")] = resolve(
            "resourcemanager.projects.getIamPolicy",
            project_verified,
            project_granted,
        )

        capability_map[i18n.capability_name("read_bucket_metadata")] = (
            i18n.value("allowed")
            if bucket_metadata.get("can_read_bucket_metadata")
            else i18n.value("denied")
        )
        return capability_map

    def _infer_access_level(self, i18n: Localization, permissions_result: dict[str, Any]) -> str:
        """Infers a coarse access level based on effective permissions."""
        if not permissions_result.get("verified"):
            return i18n.level("restricted")

        granted = set(permissions_result.get("granted_permissions", []))

        admin_requirements = {
            "storage.buckets.create",
            "storage.buckets.delete",
            "storage.objects.create",
            "storage.objects.delete",
            "resourcemanager.projects.getIamPolicy",
        }
        editor_requirements = {
            "storage.objects.create",
            "storage.objects.delete",
            "resourcemanager.projects.get",
        }
        viewer_requirements = {
            "resourcemanager.projects.get",
            "storage.objects.get",
        }

        if admin_requirements.issubset(granted):
            return i18n.level("admin")
        if editor_requirements.issubset(granted):
            return i18n.level("editor")
        if viewer_requirements.intersection(granted):
            return i18n.level("viewer")
        return i18n.level("restricted")

    def _build_recommendations(
        self,
        i18n: Localization,
        permissions_result: dict[str, Any],
    ) -> list[str]:
        """Creates actionable recommendations based on missing permissions."""
        if not permissions_result.get("verified"):
            if permissions_result.get("not_verified_reason") == "resource_manager_api_disabled":
                return [
                    "Enable Cloud Resource Manager API and run the audit again."
                    if i18n.language == "en"
                    else "Habilite a Cloud Resource Manager API e execute a auditoria novamente."
                ]
            return [
                "Permission checks could not be fully verified. Review API availability and rerun."
                if i18n.language == "en"
                else "As permissões não puderam ser verificadas completamente. Revise as APIs e rode novamente."
            ]

        missing = set(permissions_result.get("missing_permissions", []))
        recommendations: list[str] = []

        if not missing:
            recommendations.append(
                "Permissions baseline is complete for tested actions."
                if i18n.language == "en"
                else "Baseline de permissões completo para as ações testadas."
            )
            return recommendations

        if "storage.buckets.create" in missing:
            recommendations.append(
                "Ask for a role including storage.buckets.create (example: Storage Admin)."
                if i18n.language == "en"
                else "Solicite um papel com storage.buckets.create (ex.: Storage Admin)."
            )
        if "storage.objects.create" in missing:
            recommendations.append(
                "Ask for object upload permission (storage.objects.create)."
                if i18n.language == "en"
                else "Solicite permissão de upload de objetos (storage.objects.create)."
            )
        if "resourcemanager.projects.getIamPolicy" in missing:
            recommendations.append(
                "Ask for IAM policy read access on the project."
                if i18n.language == "en"
                else "Solicite acesso de leitura da política IAM do projeto."
            )

        if not recommendations:
            recommendations.append(
                "Review missing permissions and request least-privilege roles as needed."
                if i18n.language == "en"
                else "Revise as permissões ausentes e solicite papéis mínimos necessários."
            )

        return recommendations


def run_audit(base_dir: Path, config: AuditConfig, language: str) -> dict[str, Any]:
    """Runs one audit execution for a target language."""
    localized_config = AuditConfig(
        language=language,
        project_id=config.project_id,
        bucket_name_for_checks=config.bucket_name_for_checks,
        test_permissions=config.test_permissions,
    )
    i18n = Localization(base_dir, language)
    auditor = GCPAccessAuditor(localized_config)
    return auditor.run(i18n)


def summarize_report_for_terminal(report: dict[str, Any], language: str) -> dict[str, Any]:
    """Builds a compact and friendly terminal summary from the report."""
    title = next(iter(report.keys()))
    payload = report[title]

    capabilities_key = "capacidades" if language == "pt-BR" else "capabilities"
    access_level_key = "nivel_de_acesso" if language == "pt-BR" else "access_level"
    connection_key = "conexao" if language == "pt-BR" else "connection"

    capabilities = payload.get(capabilities_key, {})
    allowed_tokens = {"permitido", "allowed"}
    not_verified_tokens = {"nao_verificado", "not_verified"}
    allowed_count = sum(1 for value in capabilities.values() if str(value).lower() in allowed_tokens)
    not_verified_count = sum(
        1 for value in capabilities.values() if str(value).lower() in not_verified_tokens
    )

    connection_status = payload.get(connection_key, {}).get("status")
    return {
        "title": title,
        "connection_status": connection_status,
        "access_level": payload.get(access_level_key),
        "allowed_capabilities": allowed_count,
        "not_verified_capabilities": not_verified_count,
        "total_capabilities": len(capabilities),
    }


def build_markdown_content(
    report: dict[str, Any],
    language: str,
    executed_at: str,
    project_root: Path,
) -> str:
    """Builds a human-friendly Markdown report.

    The output is designed for non-technical readers first, while still keeping
    the full technical JSON at the end for troubleshooting.
    """
    title = next(iter(report.keys()))
    payload = report[title]

    capabilities_key = "capacidades" if language == "pt-BR" else "capabilities"
    access_level_key = "nivel_de_acesso" if language == "pt-BR" else "access_level"
    connection_key = "conexao" if language == "pt-BR" else "connection"
    recommendations_key = "acoes_recomendadas" if language == "pt-BR" else "recommended_actions"

    capabilities = payload.get(capabilities_key, {})
    allowed_tokens = {"permitido", "allowed"}
    denied_tokens = {"negado", "denied"}
    not_verified_tokens = {"nao_verificado", "not_verified"}

    allowed_items = [name for name, status in capabilities.items() if str(status).lower() in allowed_tokens]
    denied_items = [name for name, status in capabilities.items() if str(status).lower() in denied_tokens]
    not_verified_items = [
        name for name, status in capabilities.items() if str(status).lower() in not_verified_tokens
    ]

    connection_status = payload.get(connection_key, {}).get("status")
    recommendations = payload.get(recommendations_key, [])

    if language == "pt-BR":
        header_date = f"**Data de execução:** {executed_at}"
        header_path = f"**Caminho do projeto:** {project_root}"
        executive_title = "Leitura rápida"
        connection_line = f"Conexão com GCP: {connection_status}"
        level_line = f"Nível atual estimado: {payload.get(access_level_key)}"
        allowed_title = "O que foi confirmado que você pode fazer"
        denied_title = "O que foi confirmado que você não pode fazer"
        not_verified_title = "O que ainda não foi possível verificar"
        explanation_title = "Como interpretar"
        explanation_lines = [
            "- permitido: confirmado por teste real.",
            "- negado: testado e sem permissão no cenário atual.",
            "- nao_verificado: não foi possível validar, normalmente por API desabilitada ou falta de visibilidade.",
        ]
        next_steps_title = "Próximos passos recomendados"
        technical_title = "Apêndice técnico"
        structured_summary_title = "Resumo estruturado"
        full_json_title = "Relatório JSON completo"
        empty_line_message = "Nenhum item nesta categoria."
    else:
        header_date = f"**Execution date:** {executed_at}"
        header_path = f"**Project path:** {project_root}"
        executive_title = "Quick read"
        connection_line = f"GCP connection: {connection_status}"
        level_line = f"Estimated current level: {payload.get(access_level_key)}"
        allowed_title = "What was confirmed as allowed"
        denied_title = "What was confirmed as not allowed"
        not_verified_title = "What could not be verified yet"
        explanation_title = "How to read this report"
        explanation_lines = [
            "- allowed: confirmed by a real check.",
            "- denied: tested and not allowed in the current scenario.",
            "- not_verified: could not be validated, usually because an API is disabled or visibility is limited.",
        ]
        next_steps_title = "Recommended next steps"
        technical_title = "Technical appendix"
        structured_summary_title = "Structured summary"
        full_json_title = "Full JSON report"
        empty_line_message = "No items in this category."

    def render_items(items: list[str]) -> list[str]:
        if not items:
            return [f"- {empty_line_message}"]
        return [f"- {item}" for item in items]

    lines = [
        f"# {title}",
        "",
        header_date,
        header_path,
        "",
        f"## {executive_title}",
        "- " + connection_line,
        "- " + level_line,
        "",
        f"## {allowed_title}",
        *render_items(allowed_items),
        "",
        f"## {denied_title}",
        *render_items(denied_items),
        "",
        f"## {not_verified_title}",
        *render_items(not_verified_items),
        "",
        f"## {explanation_title}",
        *explanation_lines,
        "",
        f"## {next_steps_title}",
        *(recommendations if recommendations else [empty_line_message]),
        "",
        f"## {technical_title}",
        f"### {structured_summary_title}",
        "```json",
        json.dumps(capabilities, indent=2, ensure_ascii=False),
        "```",
        "",
        f"### {full_json_title}",
        "```json",
        json.dumps(report, indent=2, ensure_ascii=False),
        "```",
        "",
    ]
    return "\n".join(lines)


def export_markdown_reports(base_dir: Path, config: AuditConfig, logger: logging.Logger) -> None:
    """Exports PT-BR and EN Markdown reports automatically."""
    project_root = base_dir.parent
    executed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    outputs = [
        ("pt-BR", base_dir / "relatorio_acesso_ptbr.md"),
        ("en", base_dir / "access_report_en.md"),
    ]

    for language, target_path in outputs:
        report = run_audit(base_dir, config, language)
        content = build_markdown_content(report, language, executed_at, project_root)
        target_path.write_text(content, encoding="utf-8")
        logger.info("📄 Markdown exported: %s", target_path)


def load_config(config_path: Path) -> AuditConfig:
    """Loads the audit configuration from YAML."""
    with config_path.open("r", encoding="utf-8") as file:
        loaded = yaml.safe_load(file) or {}

    if not isinstance(loaded, dict):
        raise ValueError("config.yaml must contain a key-value mapping.")

    language = str(loaded.get("language", "pt-BR"))
    project_id = str(loaded.get("project_id", "")).strip()
    bucket_name_for_checks = str(loaded.get("bucket_name_for_checks", "")).strip()
    test_permissions = loaded.get("test_permissions") or []

    if not project_id:
        raise ValueError("config.yaml: 'project_id' is required.")
    if not bucket_name_for_checks:
        raise ValueError("config.yaml: 'bucket_name_for_checks' is required.")
    if not isinstance(test_permissions, list) or not all(
        isinstance(item, str) for item in test_permissions
    ):
        raise ValueError("config.yaml: 'test_permissions' must be a list of strings.")

    return AuditConfig(
        language=language,
        project_id=project_id,
        bucket_name_for_checks=bucket_name_for_checks,
        test_permissions=test_permissions,
    )


def main() -> None:
    """Runs the GCP access audit with friendly logs and auto TXT export."""
    logger = setup_logging()
    base_dir = Path(__file__).resolve().parent
    config = load_config(base_dir / "config.yaml")

    logger.info("🚀 Starting GCP access audit...")
    report = run_audit(base_dir, config, config.language)

    summary = summarize_report_for_terminal(report, config.language)
    logger.info("🔌 Connection status: %s", summary["connection_status"])
    logger.info("🛡️ Access level: %s", summary["access_level"])
    logger.info(
        "✅ Allowed capabilities: %s/%s",
        summary["allowed_capabilities"],
        summary["total_capabilities"],
    )
    logger.info(
        "🟡 Not verified capabilities: %s/%s",
        summary["not_verified_capabilities"],
        summary["total_capabilities"],
    )

    logger.info("🧾 Full report (JSON):")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    logger.info("📦 Exporting Markdown reports automatically (PT-BR + EN)...")
    export_markdown_reports(base_dir, config, logger)
    logger.info("🎉 Audit flow completed.")


if __name__ == "__main__":
    main()
