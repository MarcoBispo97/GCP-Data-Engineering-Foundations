# Relatório de Acesso GCP

**Data de execução:** 2026-03-15 00:29:38
**Caminho do projeto:** C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations

## Leitura rápida
- Conexão com GCP: ok
- Nível atual estimado: EDITOR

## O que foi confirmado que você pode fazer
- Criar buckets
- Deletar buckets
- Enviar arquivos (upload)
- Excluir arquivos
- Ler projeto
- Ler política IAM do projeto
- Ler metadados de bucket

## O que foi confirmado que você não pode fazer
- Ler arquivos

## O que ainda não foi possível verificar
- Nenhum item nesta categoria.

## Como interpretar
- permitido: confirmado por teste real.
- negado: testado e sem permissão no cenário atual.
- nao_verificado: não foi possível validar, normalmente por API desabilitada ou falta de visibilidade.

## Próximos passos recomendados
Solicite permissão para ler objetos (storage.objects.get).

## Apêndice técnico
### Resumo estruturado
```json
{
  "Criar buckets": "permitido",
  "Deletar buckets": "permitido",
  "Enviar arquivos (upload)": "permitido",
  "Excluir arquivos": "permitido",
  "Ler arquivos": "negado",
  "Ler projeto": "permitido",
  "Ler política IAM do projeto": "permitido",
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
      "status": "ok",
      "project_id": "global-grammar-432121-d7",
      "project_number": "439286867078",
      "lifecycle_state": "ACTIVE",
      "parent_type": null,
      "parent_id": null
    },
    "iam": {
      "status": "ok",
      "can_read_iam_policy": true,
      "binding_count": 4,
      "etag_present": true
    },
    "permissoes": {
      "status": "ok",
      "granted_permissions": [
        "resourcemanager.projects.get",
        "resourcemanager.projects.getIamPolicy",
        "storage.buckets.create",
        "storage.buckets.delete"
      ],
      "missing_permissions": [
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "verified": true,
      "not_verified_reason": null
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
      "Criar buckets": "permitido",
      "Deletar buckets": "permitido",
      "Enviar arquivos (upload)": "permitido",
      "Excluir arquivos": "permitido",
      "Ler arquivos": "negado",
      "Ler projeto": "permitido",
      "Ler política IAM do projeto": "permitido",
      "Ler metadados de bucket": "permitido"
    },
    "nivel_de_acesso": "EDITOR",
    "acoes_recomendadas": [
      "Solicite permissão para ler objetos (storage.objects.get)."
    ]
  }
}
```
