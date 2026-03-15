# Relatório de Acesso GCP

**Data de execução:** 2026-03-15 00:16:05
**Caminho do projeto:** C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations

## Leitura rápida
- Conexão com GCP: ok
- Nível atual estimado: RESTRITO

## O que foi confirmado que você pode fazer
- Deletar buckets
- Enviar arquivos (upload)
- Excluir arquivos
- Ler metadados de bucket

## O que foi confirmado que você não pode fazer
- Ler arquivos

## O que ainda não foi possível verificar
- Criar buckets
- Ler projeto
- Ler política IAM do projeto

## Como interpretar
- permitido: confirmado por teste real.
- negado: testado e sem permissão no cenário atual.
- nao_verificado: não foi possível validar, normalmente por API desabilitada ou falta de visibilidade.

## Próximos passos recomendados
Habilite a Cloud Resource Manager API e execute a auditoria novamente.

## Apêndice técnico
### Resumo estruturado
```json
{
  "Criar buckets": "nao_verificado",
  "Deletar buckets": "permitido",
  "Enviar arquivos (upload)": "permitido",
  "Excluir arquivos": "permitido",
  "Ler arquivos": "negado",
  "Ler projeto": "nao_verificado",
  "Ler política IAM do projeto": "nao_verificado",
  "Ler metadados de bucket": "permitido"
}
```

### Relatório JSON completo
```json
{
  "Relatório de Acesso GCP": {
    "conexao": {
      "status": "ok",
      "project_from_config": "global-grammar-432121-d7",
      "project_from_credentials": "global-grammar-432121-d7"
    },
    "hierarquia": {
      "status": "falhou",
      "http_status": 403,
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"consumer\": \"projects/global-grammar-432121-d7\",\n          \"serviceTitle\": \"Cloud Resource Manager API\",\n          \"service\": \"cloudresourcemanager.googleapis.com\",\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"containerInfo\": \"global-grammar-432121-d7\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n"
    },
    "iam": {
      "status": "falhou",
      "http_status": 403,
      "can_read_iam_policy": false,
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"serviceTitle\": \"Cloud Resource Manager API\",\n          \"containerInfo\": \"global-grammar-432121-d7\",\n          \"service\": \"cloudresourcemanager.googleapis.com\",\n          \"consumer\": \"projects/global-grammar-432121-d7\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n"
    },
    "permissoes": {
      "status": "falhou",
      "http_status": 403,
      "granted_permissions": [],
      "missing_permissions": [
        "resourcemanager.projects.get",
        "resourcemanager.projects.getIamPolicy",
        "storage.buckets.create",
        "storage.buckets.delete",
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"consumer\": \"projects/global-grammar-432121-d7\",\n          \"containerInfo\": \"global-grammar-432121-d7\",\n          \"service\": \"cloudresourcemanager.googleapis.com\",\n          \"serviceTitle\": \"Cloud Resource Manager API\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n",
      "verified": false,
      "not_verified_reason": "resource_manager_api_disabled"
    },
    "storage_bucket_permissions": {
      "status": "ok",
      "verified": true,
      "requested_permissions": [
        "storage.buckets.get",
        "storage.buckets.delete",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "granted_permissions": [
        "storage.buckets.delete",
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete"
      ],
      "not_verified_reason": null
    },
    "capacidades": {
      "Criar buckets": "nao_verificado",
      "Deletar buckets": "permitido",
      "Enviar arquivos (upload)": "permitido",
      "Excluir arquivos": "permitido",
      "Ler arquivos": "negado",
      "Ler projeto": "nao_verificado",
      "Ler política IAM do projeto": "nao_verificado",
      "Ler metadados de bucket": "permitido"
    },
    "nivel_de_acesso": "RESTRITO",
    "acoes_recomendadas": [
      "Habilite a Cloud Resource Manager API e execute a auditoria novamente."
    ]
  }
}
```
