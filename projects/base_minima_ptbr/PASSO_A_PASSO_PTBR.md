# Base mínima (PT-BR): criar bucket e subir arquivo

Objetivo: ter o menor código possível para entender o fluxo completo.

## 1) Entrar na pasta

```powershell
cd C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations\base_minima_ptbr
```

## 2) Instalar dependências no venv do projeto

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe -m pip install -r requirements.txt
```

## 3) Criar seu arquivo `.env`

Copie `.env.exemplo` para `.env` e ajuste os valores:

```powershell
copy .env.exemplo .env
```

Campos esperados no `.env`:
- `GCP_PROJECT_ID`
- `GCS_BUCKET_NAME`
- `LOCAL_FILE_PATH`
- `DESTINATION_BLOB_NAME` (opcional)

## 4) Criar bucket

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe 01_criar_bucket_minimo.py
```

Saída esperada:
- `Bucket criado com sucesso: ...` ou
- `Bucket já existe: ...`

## 5) Subir arquivo para o bucket

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe 02_upload_arquivo_minimo.py
```

Saída esperada:
- `Upload concluído: ... -> gs://...`

## 6) Erros comuns

- `ValueError: Defina GCP_PROJECT_ID...`
  - Faltou variável no `.env`.
- `Bucket não existe ou sem acesso`
  - Bucket não foi criado ainda ou conta sem permissão.
- `Arquivo não encontrado`
  - Caminho em `LOCAL_FILE_PATH` está inválido.

## 7) Próxima evolução sugerida

Depois dessa base mínima, evoluir para:
- logs estruturados,
- suporte a pasta inteira,
- configuração por YAML,
- classes (POO).
