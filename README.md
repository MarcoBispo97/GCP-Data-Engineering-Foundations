# GCP Data Engineering Foundations

## 🇧🇷 Português (PT-BR)

Este projeto reúne exercícios e anotações práticas de Google Cloud Platform (GCP), com foco em Cloud Storage e configuração de ambiente local.

### Estrutura principal
- `01_create_bucket.py`: script Python para criar bucket no Cloud Storage.
- `0_gcp_commands_utils.ipynb`: comandos e utilitários GCP.
- `1-Data_Engineering_Fundations.ipynb`: fundamentos de Data Engineering.
- `2-Google_cloud-data-storage.ipynb`: práticas de Cloud Storage.
- `settings_gcp.ipynb`: documentação bilíngue (PT/EN) do setup realizado.
- `settings_gcp_ptbr.ipynb`: documentação apenas em português.
- `settings_gcp_en.ipynb`: documentation in English only.

### Pré-requisitos
- Python 3.14+
- Git Bash (ou PowerShell)
- Google Cloud SDK (`gcloud`)
- Projeto GCP ativo

### Setup rápido
1. Criar/ativar ambiente virtual:
   - Git Bash: `source venv/Scripts/activate`
2. Login no GCP:
   - `gcloud auth login`
3. Configurar ADC para bibliotecas Python:
   - `gcloud auth application-default login`
4. Definir projeto padrão:
   - `gcloud config set project global-grammar-432121-d7`
5. Definir quota project para ADC:
   - `gcloud auth application-default set-quota-project global-grammar-432121-d7`

### Segurança
- Não compartilhar códigos de verificação OAuth.
- Não compartilhar tokens de acesso.
- Não versionar chaves JSON de service account.

---

## 🇺🇸 English

This project contains practical Google Cloud Platform (GCP) exercises and notes, focused on Cloud Storage and local environment setup.

### Main structure
- `01_create_bucket.py`: Python script to create a Cloud Storage bucket.
- `0_gcp_commands_utils.ipynb`: GCP helper commands and utilities.
- `1-Data_Engineering_Fundations.ipynb`: Data Engineering foundations.
- `2-Google_cloud-data-storage.ipynb`: Cloud Storage practices.
- `settings_gcp.ipynb`: bilingual (PT/EN) setup documentation.
- `settings_gcp_ptbr.ipynb`: Portuguese-only setup documentation.
- `settings_gcp_en.ipynb`: English-only setup documentation.

### Prerequisites
- Python 3.14+
- Git Bash (or PowerShell)
- Google Cloud SDK (`gcloud`)
- Active GCP project

### Quick setup
1. Create/activate virtual environment:
   - Git Bash: `source venv/Scripts/activate`
2. Sign in to GCP:
   - `gcloud auth login`
3. Configure ADC for Python libraries:
   - `gcloud auth application-default login`
4. Set default project:
   - `gcloud config set project global-grammar-432121-d7`
5. Set ADC quota project:
   - `gcloud auth application-default set-quota-project global-grammar-432121-d7`

### Security
- Do not share OAuth verification codes.
- Do not share access tokens.
- Do not commit service account JSON keys.
