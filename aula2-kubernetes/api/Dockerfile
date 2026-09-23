# Imagem base: Python enxuto, a mesma da Aula 1
FROM python:3.12-slim

# A versão da imagem entra como argumento de build (--build-arg VERSAO=v3)
# e vira variável de ambiente que a API lê em /versao. v2 e v3 são este
# mesmo Dockerfile, construído duas vezes com valores diferentes.
ARG VERSAO=v2
ENV VERSAO=${VERSAO}

# curl dentro da imagem: o roteiro usa
#   kubectl exec -it sentiment-api -- curl -s localhost:8000/health
# para mostrar que a API responde de dentro do pod. A imagem slim não traz.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependências antes do código: a camada lenta fica em cache (Aula 1)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código e modelo
COPY api.py modelo.pkl ./

# A porta que o uvicorn escuta: é o containerPort do pod.yaml
# e o targetPort do service.yaml
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
