# GCP Access Audit

Ferramenta de auditoria para entender, de forma simples, o que a conta atual consegue fazer no Google Cloud.

Audit tool to understand, in a simple way, what the current account can do in Google Cloud.

---

## 🇧🇷 Português (PT-BR)

### O que esta pasta entrega

- Um script Python que testa conexão com o GCP.
- Verificações de acesso ao projeto, IAM e permissões de Storage.
- Um resumo amigável no terminal.
- Relatórios em Markdown prontos para leitura humana.

### Arquivos principais

- `gcp_access_audit.py`: script principal da auditoria.
- `config.yaml`: projeto, bucket de checagem, idioma e permissões a testar.
- `messages_pt-BR.yaml`: textos localizados em português.
- `messages_en.yaml`: textos localizados em inglês.
- `requirements.txt`: dependências da auditoria.
- `relatorio_acesso_ptbr.md`: relatório em português gerado automaticamente.
- `access_report_en.md`: report in English generated automatically.

### Como executar

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/gcp_access_audit/gcp_access_audit.py
```

### O que acontece quando você roda

O script:

- testa a conexão com o GCP;
- verifica visibilidade de projeto e IAM;
- testa permissões reais no bucket configurado;
- mostra um resumo executivo no terminal;
- gera relatórios em Markdown em PT-BR e EN.

### Como interpretar o relatório

- `permitido`: foi testado e confirmado.
- `negado`: foi testado e a permissão não está disponível.
- `nao_verificado`: não foi possível validar, normalmente por API desabilitada ou falta de visibilidade.

### Quando o resultado pode parecer “mais restrito” do que a realidade

Isso acontece quando alguma API necessária para auditoria não está habilitada.

Exemplo comum:

- `Cloud Resource Manager API` desabilitada.

Nesse caso, o relatório pode marcar parte das permissões como `nao_verificado`, mesmo que você consiga operar normalmente no Cloud Storage.

### Trocar idioma

No `config.yaml`:

- `language: pt-BR`
- `language: en`

### Resultado esperado

No terminal:

- status da conexão;
- nível estimado de acesso;
- quantidade de capacidades permitidas;
- quantidade de capacidades não verificadas.

Nos arquivos gerados:

- leitura executiva para não devs;
- apêndice técnico em JSON.

---

## 🇺🇸 English

### What this folder provides

- A Python script that tests GCP connectivity.
- Access checks for project visibility, IAM, and Storage permissions.
- A friendly terminal summary.
- Human-readable Markdown reports.

### Main files

- `gcp_access_audit.py`: main audit script.
- `config.yaml`: project, check bucket, language, and permissions to test.
- `messages_pt-BR.yaml`: Portuguese localized texts.
- `messages_en.yaml`: English localized texts.
- `requirements.txt`: audit dependencies.
- `relatorio_acesso_ptbr.md`: automatically generated Portuguese report.
- `access_report_en.md`: automatically generated English report.

### How to run

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/gcp_access_audit/gcp_access_audit.py
```

### What happens when you run it

The script:

- tests GCP connectivity;
- checks project and IAM visibility;
- tests real permissions against the configured bucket;
- prints an executive-style summary in the terminal;
- generates Markdown reports in PT-BR and EN.

### How to read the report

- `allowed`: tested and confirmed.
- `denied`: tested and not available.
- `not_verified`: could not be validated, usually because an API is disabled or visibility is limited.

### When results may look more restrictive than reality

This usually happens when a required audit API is disabled.

Common example:

- `Cloud Resource Manager API` is disabled.

In that case, some permissions may appear as `not_verified`, even when Cloud Storage operations are working.

### Change the language

In `config.yaml`:

- `language: pt-BR`
- `language: en`

### Expected output

In the terminal:

- connection status;
- estimated access level;
- number of allowed capabilities;
- number of not-verified capabilities.

In the generated files:

- executive summary for non-developers;
- technical JSON appendix.
