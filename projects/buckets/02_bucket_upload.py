from dataclasses import dataclass
from pathlib import Path
import logging
import os
from typing import Any, Optional

from dotenv import load_dotenv
from google.cloud import storage
import yaml

load_dotenv()


def setup_logging(level: int = logging.INFO) -> None:
    """Configures the root logging format and level.

    Args:
        level: Global logging level.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )


@dataclass(frozen=True)
class AppConfig:
    """Represents environment configuration for GCS upload operations.

    Attributes:
        project_id: Google Cloud project ID.
        bucket_name: Target GCS bucket name.
        source_path: Local source path (single file or folder).
        destination_blob_name: Optional destination object name for single-file upload.
        destination_prefix: Optional prefix (folder path) inside the bucket.
        recursive: If True and source_path is a folder, uploads files recursively.
        service_account_key_path: Optional service account JSON path.
    """

    project_id: str
    bucket_name: str
    source_path: str
    destination_blob_name: Optional[str] = None
    destination_prefix: str = ""
    recursive: bool = True
    service_account_key_path: Optional[str] = None
    config_file_path: str = "gcs_upload.yaml"

    @classmethod
    def from_sources(cls) -> "AppConfig":
        """Builds configuration from YAML file and environment variables.

        Configuration precedence (highest to lowest):
        1. Environment variables
        2. YAML file values
        3. Hard-coded defaults

        Environment variables:
            GCP_PROJECT_ID / GOOGLE_CLOUD_PROJECT
            GCS_BUCKET_NAME
            LOCAL_FILE_PATH
            GCS_DESTINATION_BLOB
            GCS_DESTINATION_PREFIX
            GCS_RECURSIVE
            GOOGLE_APPLICATION_CREDENTIALS
            GCS_UPLOAD_CONFIG

        Returns:
            A validated AppConfig instance.

        Raises:
            ValueError: If required environment variables are missing.
            FileNotFoundError: If the source path does not exist.
        """
        config_logger = logging.getLogger("app.config")

        config_file_path = os.getenv("GCS_UPLOAD_CONFIG", "gcs_upload.yaml")
        yaml_data = cls._load_yaml_config(config_file_path, config_logger)

        project_id = (
            os.getenv("GCP_PROJECT_ID")
            or os.getenv("GOOGLE_CLOUD_PROJECT")
            or str(yaml_data.get("project_id", "")).strip()
        )
        bucket_name = os.getenv("GCS_BUCKET_NAME") or str(yaml_data.get("bucket_name", "")).strip()
        source_path_raw = (
            os.getenv("LOCAL_FILE_PATH")
            or str(yaml_data.get("source_path", "")).strip()
            or "test_shakesper.txt"
        )
        destination_blob_name_raw = os.getenv("GCS_DESTINATION_BLOB")
        if destination_blob_name_raw is None:
            destination_blob_name_raw = yaml_data.get("destination_blob_name")

        destination_prefix = (
            os.getenv("GCS_DESTINATION_PREFIX")
            or str(yaml_data.get("destination_prefix", "")).strip()
        )

        recursive_raw: Any = os.getenv("GCS_RECURSIVE")
        if recursive_raw is None:
            recursive_raw = yaml_data.get("recursive", True)
        recursive = cls._to_bool(recursive_raw)

        service_account_key_path = (
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            or str(yaml_data.get("service_account_key_path", "")).strip()
            or None
        )

        if not project_id:
            raise ValueError(
                "Set GCP_PROJECT_ID (or GOOGLE_CLOUD_PROJECT) in environment variables."
            )
        if not bucket_name:
            raise ValueError("Set GCS_BUCKET_NAME in environment variables.")

        source_path = Path(source_path_raw)
        if not source_path.exists():
            raise FileNotFoundError(
                f"Source path was not found: {source_path.resolve()}"
            )

        config_logger.info("Environment configuration loaded successfully.")
        config_logger.debug(
            "Config values project_id=%s bucket_name=%s source_path=%s destination_blob=%s destination_prefix=%s recursive=%s using_key=%s",
            project_id,
            bucket_name,
            str(source_path),
            destination_blob_name_raw,
            destination_prefix,
            recursive,
            bool(service_account_key_path),
        )

        return cls(
            project_id=project_id,
            bucket_name=bucket_name,
            source_path=str(source_path),
            destination_blob_name=(str(destination_blob_name_raw).strip() or None)
            if destination_blob_name_raw is not None
            else None,
            destination_prefix=destination_prefix.strip("/"),
            recursive=recursive,
            service_account_key_path=service_account_key_path,
            config_file_path=config_file_path,
        )

    @staticmethod
    def _load_yaml_config(config_file_path: str, logger: logging.Logger) -> dict[str, Any]:
        """Loads YAML configuration from disk.

        Args:
            config_file_path: YAML config path.
            logger: Logger used for status messages.

        Returns:
            Parsed YAML dictionary or empty dict if file does not exist.

        Raises:
            ValueError: If YAML content is invalid.
        """
        path = Path(config_file_path)
        if not path.exists():
            logger.info(
                "YAML config '%s' not found. Falling back to environment/default values.",
                config_file_path,
            )
            return {}

        logger.info("Loading YAML config from '%s'.", path)
        with path.open("r", encoding="utf-8") as config_file:
            loaded = yaml.safe_load(config_file) or {}

        if not isinstance(loaded, dict):
            raise ValueError("YAML config must be a key-value mapping.")

        return loaded

    @staticmethod
    def _to_bool(value: Any) -> bool:
        """Converts input values to boolean.

        Args:
            value: Input value.

        Returns:
            Parsed boolean value.
        """
        if isinstance(value, bool):
            return value
        if value is None:
            return False

        normalized = str(value).strip().lower()
        return normalized in {"1", "true", "yes", "y", "on"}


class StorageClientFactory:
    """Creates configured `google.cloud.storage.Client` instances."""

    def __init__(self, config: AppConfig) -> None:
        """Initializes the factory.

        Args:
            config: Application configuration.
        """
        self.config = config
        self.logger = logging.getLogger("app.auth")

    def build(self) -> storage.Client:
        """Builds the storage client using ADC or service account JSON.

        Returns:
            A configured Storage client.
        """
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", self.config.project_id)

        if self.config.service_account_key_path:
            self.logger.info("Creating storage client using service account JSON.")
            return storage.Client.from_service_account_json(
                self.config.service_account_key_path,
                project=self.config.project_id,
            )

        self.logger.info("Creating storage client using Application Default Credentials (ADC).")
        return storage.Client(project=self.config.project_id)


class UploadService:
    """Provides file upload operations to a GCS bucket."""

    def __init__(self, client: storage.Client, config: AppConfig) -> None:
        """Initializes the service.

        Args:
            client: Google Cloud Storage client.
            config: Application configuration.
        """
        self.client = client
        self.config = config
        self.connection_logger = logging.getLogger("app.connection")
        self.upload_logger = logging.getLogger("app.upload")

    def test_connection(self) -> None:
        """Tests GCS connection by requesting project buckets metadata.

        Raises:
            Exception: If the API call fails for auth/network/permission reasons.
        """
        self.connection_logger.info(
            "Testing GCS connection for project '%s'.",
            self.config.project_id,
        )
        self.client.list_buckets(project=self.config.project_id, max_results=1)
        self.connection_logger.info("GCS connection test succeeded.")

    def ensure_bucket_exists(self) -> storage.Bucket:
        """Validates that the target bucket exists and is accessible.

        Returns:
            The target bucket instance.

        Raises:
            ValueError: If the bucket does not exist or is inaccessible.
        """
        self.upload_logger.info(
            "Checking access to bucket '%s'.",
            self.config.bucket_name,
        )
        bucket = self.client.lookup_bucket(self.config.bucket_name)
        if bucket is None:
            raise ValueError(
                f"Bucket '{self.config.bucket_name}' was not found or is not accessible."
            )

        self.upload_logger.info("Bucket '%s' is available.", self.config.bucket_name)
        return bucket

    def upload_from_source(self) -> None:
        """Uploads one or multiple local files to the target GCS bucket."""
        self.test_connection()
        bucket = self.ensure_bucket_exists()

        source_path = Path(self.config.source_path)
        file_pairs = self._resolve_upload_targets(source_path)

        self.upload_logger.info("Resolved %d file(s) to upload.", len(file_pairs))
        for local_path, blob_name in file_pairs:
            blob = bucket.blob(blob_name)
            self.upload_logger.info(
                "Uploading local file '%s' to 'gs://%s/%s'.",
                str(local_path),
                self.config.bucket_name,
                blob_name,
            )
            blob.upload_from_filename(str(local_path))

        self.upload_logger.info("Upload completed successfully.")

    def _resolve_upload_targets(self, source_path: Path) -> list[tuple[Path, str]]:
        """Builds local-file and destination-blob pairs for upload.

        Args:
            source_path: Source file or directory path.

        Returns:
            A list of tuples containing local file path and destination blob name.

        Raises:
            ValueError: If source path type is unsupported or no files are found.
        """
        if source_path.is_file():
            blob_name = self.config.destination_blob_name or source_path.name
            blob_name = self._with_prefix(blob_name)
            return [(source_path, blob_name)]

        if source_path.is_dir():
            if self.config.recursive:
                files = [path for path in source_path.rglob("*") if path.is_file()]
            else:
                files = [path for path in source_path.glob("*") if path.is_file()]

            if not files:
                raise ValueError(f"No files found inside folder: {source_path}")

            pairs: list[tuple[Path, str]] = []
            for file_path in files:
                relative_blob = file_path.relative_to(source_path).as_posix()
                pairs.append((file_path, self._with_prefix(relative_blob)))
            return pairs

        raise ValueError(f"Unsupported source path: {source_path}")

    def _with_prefix(self, blob_name: str) -> str:
        """Adds destination prefix to blob name when configured.

        Args:
            blob_name: Blob name without prefix.

        Returns:
            Final blob name with optional prefix.
        """
        if not self.config.destination_prefix:
            return blob_name
        return f"{self.config.destination_prefix}/{blob_name}"


def main() -> None:
    """Runs the file upload flow."""
    setup_logging()
    app_logger = logging.getLogger("app.main")

    config = AppConfig.from_sources()
    client = StorageClientFactory(config).build()
    service = UploadService(client, config)

    app_logger.info("Starting upload flow.")
    service.upload_from_source()
    app_logger.info("Upload flow finished.")


if __name__ == "__main__":
    main()
