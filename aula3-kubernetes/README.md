# Aula 3 — Kubernetes II: réplicas, Deployment, rolling update e rollback

A mesma API, agora com três réplicas mantidas vivas por um Deployment, um Service dividindo o tráfego entre elas, e uma troca de versão (v2 → v3) sem derrubar a API, com direito a voltar atrás.

| Arquivo | O que é |
|---|---|
| `ROTEIRO.md` | **Comece por aqui:** o passo a passo da prática no Azure |
| `ATIVIDADE.md` | A atividade avaliativa da semana |
| `manifests/deployment.yaml` | O Deployment: 3 réplicas, requests/limits, probes e estratégia RollingUpdate |
| `manifests/service.yaml` | O mesmo Service da Aula 2, sem uma vírgula de diferença |

## As imagens

| Imagem | `/versao` responde |
|---|---|
| `ghcr.io/rodolfo-s-antunes/sentiment-api:v2` | `{"versao":"v2"}` — a versão inicial do Deployment |
| `ghcr.io/rodolfo-s-antunes/sentiment-api:v3` | `{"versao":"v3"}` — o destino do rolling update |

As duas são o mesmo código ([`../aula2-kubernetes/api/`](../aula2-kubernetes/api/)), construído com `--build-arg VERSAO` diferente. Nada muda no modelo nem nos endpoints: a única diferença observável é o texto da versão, e é exatamente isso que o `curl` em loop da Etapa 9 mostra alternando durante a troca.
