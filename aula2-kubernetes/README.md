# Aula 2 — Kubernetes I: Pod e Service no AKS

A API de sentimento da Aula 1, agora dentro de um cluster Kubernetes gerenciado (AKS), exposta em um IP público por um Service. Nada é construído nesta aula: a imagem já está pronta e pública no GHCR.

| Arquivo | O que é |
|---|---|
| `ROTEIRO.md` | **Comece por aqui:** o passo a passo da prática no Azure |
| `ATIVIDADE.md` | A atividade avaliativa da semana |
| `manifests/pod.yaml` | O Pod da API. Troque `SUBSTITUA` pelos nomes da dupla antes de aplicar |
| `manifests/service.yaml` | O Service `LoadBalancer`: porta 80 pública → 8000 do container |
| `manifests/exemplo-configmap.yaml` | ConfigMap e Secret: exemplo que ficou só na teoria |
| `api/` | O código da imagem `sentiment-api:v2` (referência; a mesma receita gera a `v3` da Aula 3) |

## A imagem

`ghcr.io/rodolfo-s-antunes/sentiment-api:v2` é a API da Aula 1 com três endpoints a mais, pensados para o cluster:

| Endpoint | Resposta | Para quê |
|---|---|---|
| `GET /health` | `{"status":"ok","modelo_carregado":true}` | As probes do Kubernetes (Aula 3) perguntam aqui |
| `GET /versao` | `{"versao":"v2"}` | Ver qual imagem responde; muda no rolling update da Aula 3 |
| `GET /hostname` | `{"hostname":"sentiment-api"}` | O nome do pod que respondeu: a prova do load balancing na Aula 3 |
| `POST /prediz` | `{"sentimento":"positivo","confianca":0.93}` | A inferência, igual à Aula 1 |

A `v3` é exatamente o mesmo código construído com `--build-arg VERSAO=v3`. O build acontece no GitHub Actions ([`.github/workflows/build-aula2.yml`](../.github/workflows/build-aula2.yml)).

## Executar a API localmente (opcional, fora da aula)

```bash
cd api
pip install -r requirements.txt
VERSAO=dev uvicorn api:app --host 0.0.0.0 --port 8000
# abra http://localhost:8000/docs
```
