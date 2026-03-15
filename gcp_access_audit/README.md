# GCP Access Audit

Script em Python para auditar seu nível de acesso no GCP com saída amigável no terminal e exportar TXT automaticamente em PT-BR e EN.

## Arquivos
- `gcp_access_audit.py`: script único que audita e exporta os dois TXT automaticamente.
- `config.yaml`: configura projeto, bucket de checagem, idioma e permissões testadas.
- `messages_pt-BR.yaml`: labels/valores em português.
- `messages_en.yaml`: labels/values in English.
- `requirements.txt`: dependências do módulo.

## Como executar

```powershell
C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/venv/Scripts/python.exe C:/Users/marco/Documents/code_classes/GCP-Data-Engineering-Foundations/gcp_access_audit/gcp_access_audit.py
```

Ao executar, o script:
- mostra um resumo amigável no terminal (status de conexão, nível e capacidades liberadas);
- imprime o JSON completo;
- gera os arquivos `relatorio_acesso_ptbr.txt` e `access_report_en.txt`.

## Trocar idioma por YAML
No arquivo `config.yaml`:

- Português: `language: pt-BR`
- Inglês: `language: en`

Depois rode o mesmo comando novamente.

## O que o relatório mostra
- conexão
- hierarquia do projeto
- visibilidade de IAM
- permissões concedidas/ausentes
- capacidades (pode criar/deletar bucket, upload, etc.)
- nível de acesso inferido (`ADMINISTRADOR`, `EDITOR`, `LEITOR`, `RESTRITO`)
- ações recomendadas

## Observação importante
Se aparecer erro 403 com `SERVICE_DISABLED`, habilite a API **Cloud Resource Manager API** no projeto e rode novamente.
