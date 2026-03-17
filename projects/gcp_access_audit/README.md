# GCP Access Audit

Ferramenta para auditar, por API, o que a identidade autenticada consegue ver e fazer no projeto GCP e no bucket configurado.

Tool to audit, through API checks, what the authenticated identity can see and do in the target GCP project and bucket.

---

## 🇧🇷 Português (PT-BR)

### Objetivo

Esta pasta concentra uma auditoria prática para responder três perguntas de forma objetiva:

- a conexão com o GCP está funcionando;
- o projeto e a política IAM do projeto estão visíveis;
- quais ações de Storage estão efetivamente permitidas no bucket analisado.

### O que a auditoria verifica

- Conectividade com as credenciais locais atuais.
- Leitura de metadados do projeto via Cloud Resource Manager API.
- Leitura da política IAM do projeto.
- `testIamPermissions` no projeto para permissões configuradas.
- `test_iam_permissions` no bucket para validar ações de bucket e objetos.
- Geração de um nível estimado de acesso com base nas permissões confirmadas.

### Arquivos principais

- `gcp_access_audit.py`: script principal.
- `config.yaml`: idioma, projeto, bucket de referência e permissões a testar.
- `messages_pt-BR.yaml`: rótulos e mensagens em português.
- `messages_en.yaml`: rótulos e mensagens em inglês.
- `relatorio_acesso_ptbr.md`: relatório em português gerado automaticamente.
- `access_report_en.md`: relatório em inglês gerado automaticamente.

### Como executar

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/gcp_access_audit/gcp_access_audit.py
```

### Como interpretar a saída

- `permitido`: a ação foi confirmada por chamada de API.
- `negado`: a API respondeu sem essa permissão no contexto atual.
- `nao_verificado`: faltou visibilidade suficiente para concluir o teste.

### Como o nível de acesso é calculado

- `ADMIN`: consegue criar e deletar bucket, enviar, excluir e ler objetos, além de ler IAM do projeto.
- `EDITOR`: consegue alterar objetos e possui visibilidade mínima de projeto ou bucket.
- `LEITOR`: consegue apenas leitura de projeto, bucket ou objetos.
- `RESTRITO`: a auditoria não conseguiu confirmar leitura ou alteração relevantes.

### Limitações importantes

- O resultado é uma estimativa baseada apenas nas permissões testadas.
- Permissões de projeto e de bucket podem divergir; por isso o relatório mostra as duas visões.
- Se a `Cloud Resource Manager API` estiver desabilitada, parte da análise pode cair para `nao_verificado`.

### Ajustes mais comuns

No `config.yaml` você normalmente altera:

- `language`
- `project_id`
- `bucket_name_for_checks`
- `test_permissions`

---

## 🇺🇸 English

### Purpose

This folder contains a practical audit that answers three direct questions:

- is GCP connectivity working;
- are project metadata and project IAM policy visible;
- which Storage actions are effectively allowed on the configured bucket.

### What the audit checks

- Connectivity with the current local credentials.
- Project metadata visibility through Cloud Resource Manager API.
- Project IAM policy visibility.
- `testIamPermissions` at project level for configured permissions.
- `test_iam_permissions` at bucket level for bucket and object actions.
- A derived access level based on the permissions that were actually confirmed.

### Main files

- `gcp_access_audit.py`: main script.
- `config.yaml`: language, project, reference bucket, and permissions to test.
- `messages_pt-BR.yaml`: Portuguese labels and messages.
- `messages_en.yaml`: English labels and messages.
- `relatorio_acesso_ptbr.md`: auto-generated Portuguese report.
- `access_report_en.md`: auto-generated English report.

### How to run

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/gcp_access_audit/gcp_access_audit.py
```

### How to read the output

- `allowed`: the action was confirmed through an API check.
- `denied`: the API check completed and the permission was not available.
- `not_verified`: visibility was not sufficient to conclude the test.

### How the access level is derived

- `ADMIN`: can create and delete buckets, upload, delete, and read objects, and read project IAM.
- `EDITOR`: can modify objects and has minimum project or bucket visibility.
- `VIEWER`: can only read project, bucket, or objects.
- `RESTRICTED`: the audit could not confirm meaningful read or write access.

### Important limitations

- The result is an estimate based only on the permissions being tested.
- Project-level and bucket-level permissions may differ, so the report shows both perspectives.
- If `Cloud Resource Manager API` is disabled, part of the audit may fall back to `not_verified`.

### Most common config changes

In `config.yaml`, you will usually adjust:

- `language`
- `project_id`
- `bucket_name_for_checks`
- `test_permissions`
