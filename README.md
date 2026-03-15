# GCP Data Engineering Foundations

## 🇧🇷 Português (PT-BR)

Repositório de estudo prático para fundamentos de Data Engineering no GCP, com foco em configuração local, Google Cloud Storage e auditoria de acesso baseada em API.

### O que você encontra aqui

- Notebooks de apoio para setup e estudo de GCP.
- Scripts Python para criar buckets e fazer upload de arquivos.
- Uma trilha mínima em PT-BR para repetir o fluxo do zero.
- Uma auditoria de acesso que gera relatórios executivos em Markdown.

### Estrutura do projeto

- `0_gcp_commands_utils.ipynb`: comandos úteis de GCP para consulta rápida.
- `1-Data_Engineering_Fundations.ipynb`: anotações e fundamentos de Data Engineering.
- `2-Google_cloud-data-storage.ipynb`: práticas com Cloud Storage.
- `settings_gcp_ptbr.ipynb`: passo a passo de setup em português.
- `settings_gcp_en.ipynb`: setup equivalente em inglês.
- `buckets/`: scripts mais completos para criação de bucket e upload.
- `base_minima_ptbr/`: versão enxuta para aprender o fluxo com menos abstração.
- `gcp_access_audit/`: auditoria de acesso GCP com saída no terminal e relatórios em Markdown.

### Fluxo recomendado

1. Configure autenticação local com `gcloud auth login`.
2. Configure ADC com `gcloud auth application-default login`.
3. Defina o projeto com `gcloud config set project global-grammar-432121-d7`.
4. Revise os notebooks de setup.
5. Use os scripts em `buckets/` ou `base_minima_ptbr/`.
6. Rode a auditoria em `gcp_access_audit/` para verificar o que a conta consegue fazer.

### Pré-requisitos

- Python 3.14+
- Google Cloud SDK (`gcloud`)
- Git Bash ou PowerShell
- Projeto GCP ativo
- Credenciais locais válidas via ADC

### Segurança

- Não compartilhe códigos OAuth, tokens ou chaves JSON.
- Prefira ADC para desenvolvimento local.
- Não versione arquivos sensíveis em `.env` ou credenciais exportadas.

---

## 🇺🇸 English

Practical study repository for GCP Data Engineering foundations, focused on local setup, Google Cloud Storage, and API-based access auditing.

### What is included

- Support notebooks for GCP setup and study.
- Python scripts for bucket creation and file uploads.
- A minimal PT-BR track to replay the workflow with less abstraction.
- An access auditor that produces executive Markdown reports.

### Project structure

- `0_gcp_commands_utils.ipynb`: useful GCP commands for quick reference.
- `1-Data_Engineering_Fundations.ipynb`: notes and Data Engineering foundations.
- `2-Google_cloud-data-storage.ipynb`: Cloud Storage practice material.
- `settings_gcp_ptbr.ipynb`: Portuguese setup walkthrough.
- `settings_gcp_en.ipynb`: English setup walkthrough.
- `buckets/`: more complete scripts for bucket creation and uploads.
- `base_minima_ptbr/`: lean learning path with less abstraction.
- `gcp_access_audit/`: GCP access audit with terminal output and Markdown reports.

### Recommended flow

1. Configure local authentication with `gcloud auth login`.
2. Configure ADC with `gcloud auth application-default login`.
3. Set the project with `gcloud config set project global-grammar-432121-d7`.
4. Review the setup notebooks.
5. Use the scripts under `buckets/` or `base_minima_ptbr/`.
6. Run the audit under `gcp_access_audit/` to verify what the account can do.

### Prerequisites

- Python 3.14+
- Google Cloud SDK (`gcloud`)
- Git Bash or PowerShell
- Active GCP project
- Valid local ADC credentials

### Security

- Do not share OAuth codes, tokens, or JSON keys.
- Prefer ADC for local development.
- Do not commit sensitive `.env` values or exported credentials.
