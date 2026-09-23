"""
API de análise de sentimento — imagem v2/v3 (Aulas 2 e 3, Kubernetes).

É a mesma API da Aula 1 com três endpoints a mais, pensados para o cluster:

    GET  /health    -> a readiness/liveness probe do Kubernetes pergunta aqui
    GET  /versao    -> mostra qual imagem está respondendo (v2 ou v3)
    GET  /hostname  -> devolve o nome do pod: a prova visual do load balancing
    POST /prediz    -> a inferência, igual à Aula 1

A versão NÃO está escrita no código: vem da variável de ambiente VERSAO,
gravada na imagem em tempo de build (ARG/ENV no Dockerfile). v2 e v3 são
o mesmo código, com esse valor diferente. É de propósito: na Aula 3, o
rolling update troca a imagem e o /versao mostra a troca acontecendo.

Executar localmente:  uvicorn api:app --host 0.0.0.0 --port 8000
Documentação:         http://localhost:8000/docs
"""

import os
import socket

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# Definida no Dockerfile (ENV VERSAO). Fora do container, assume "dev".
VERSAO = os.getenv("VERSAO", "dev")

app = FastAPI(
    title="API de Sentimento — Infraestrutura Computacional para IA",
    description="Aulas 2 e 3: a API da Aula 1 rodando dentro do Kubernetes.",
    version=VERSAO,
)

# O modelo é carregado UMA vez, quando o container inicia. Enquanto esta
# linha não termina, a API não responde — e é por isso que o Kubernetes
# pergunta em /health antes de mandar tráfego para o pod (readiness probe).
modelo = joblib.load("modelo.pkl")


class Entrada(BaseModel):
    texto: str


class Saida(BaseModel):
    sentimento: str
    confianca: float


@app.get("/")
def raiz():
    """Página inicial: um resumo do serviço."""
    return {
        "servico": "api-de-sentimento",
        "versao": VERSAO,
        "hostname": socket.gethostname(),
        "endpoints": ["/health", "/versao", "/hostname", "/prediz", "/docs"],
    }


@app.get("/health")
def health():
    """
    Verificação de saúde usada pelas probes do Kubernetes.

    Responde 200 só se o modelo está em memória. Não consulta banco nem
    serviço externo: uma dependência lenta derrubaria todos os pods juntos.
    """
    return {"status": "ok", "modelo_carregado": modelo is not None}


@app.get("/versao")
def versao():
    """Qual versão da imagem está respondendo. Muda durante o rolling update."""
    return {"versao": VERSAO}


@app.get("/hostname")
def hostname():
    """
    Nome da máquina que respondeu. Dentro do Kubernetes, o hostname do
    container é o nome do pod: com várias réplicas atrás de um Service,
    chamadas seguidas devolvem nomes diferentes.
    """
    return {"hostname": socket.gethostname()}


@app.post("/prediz", response_model=Saida)
def prediz(entrada: Entrada):
    """Classifica o sentimento de uma frase em português."""
    probabilidades = modelo.predict_proba([entrada.texto])[0]
    indice = probabilidades.argmax()
    return Saida(
        sentimento=modelo.classes_[indice],
        confianca=round(float(probabilidades[indice]), 4),
    )
