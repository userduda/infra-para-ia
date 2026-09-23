"""
Treina o modelo de análise de sentimento usado na Aula 1.

O objetivo NÃO é ter o melhor modelo do mundo, e sim um modelo leve,
rápido e didático para ser empacotado em um container. O pipeline é:

    TF-IDF (transforma texto em números) -> Regressão Logística (classifica)

Para retreinar:  python treinar_modelo.py
Saída:           modelo.pkl (usado pela API em api.py)
"""

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------------------------
# Dataset didático: frases curtas em português rotuladas como
# "positivo" ou "negativo". Em um projeto real, isso viria de um
# arquivo/banco com milhares de exemplos (tema da Aula 5: object storage!).
# ---------------------------------------------------------------------------

FRASES_POSITIVAS = [
    "adorei o curso",
    "o professor explica muito bem",
    "a aula de hoje foi excelente",
    "gostei muito da experiência",
    "produto de ótima qualidade",
    "atendimento rápido e eficiente",
    "superou todas as minhas expectativas",
    "recomendo para todo mundo",
    "muito bom, voltarei com certeza",
    "a entrega chegou antes do prazo",
    "estou muito satisfeito com o resultado",
    "melhor compra que fiz este ano",
    "equipe atenciosa e prestativa",
    "funcionou perfeitamente desde o início",
    "conteúdo claro e bem organizado",
    "que experiência maravilhosa",
    "amei cada detalhe",
    "vale muito a pena",
    "simplesmente perfeito",
    "fiquei impressionado com a qualidade",
    "o suporte resolveu meu problema na hora",
    "interface bonita e fácil de usar",
    "excelente custo benefício",
    "tudo funcionou como prometido",
    "o material da disciplina é muito bom",
    "aprendi bastante nessa aula",
    "as atividades práticas foram divertidas",
    "nota dez, sem defeitos",
    "chegou tudo certinho e bem embalado",
    "o serviço melhorou muito ultimamente",
    "estou encantado com esse produto",
    "a plataforma é rápida e estável",
    "ótima didática e ótimos exemplos",
    "me senti muito bem atendido",
    "essa ferramenta facilitou meu trabalho",
    "resultado incrível, parabéns à equipe",
    "muito prático e intuitivo",
    "a comida estava deliciosa",
    "ambiente agradável e organizado",
    "voltarei a comprar com certeza",
    "que aula sensacional",
    "o laboratório foi muito bem conduzido",
    "gostei do ritmo e da clareza",
    "tudo excelente do começo ao fim",
    "experiência positiva em todos os sentidos",
    "o aplicativo é leve e funciona bem",
    "cumpriu tudo o que prometeu",
    "estou muito feliz com a escolha",
    "serviço impecável",
    "foi a melhor decisão que tomei",
    "o time foi super gentil comigo",
    "a qualidade do som é fantástica",
    "documentação clara e completa",
    "instalação simples e sem dor de cabeça",
    "desempenho acima do esperado",
    "adorei a nova versão",
    "muito eficiente, economizou meu tempo",
    "as explicações foram claras e objetivas",
    "produto durável e bem construído",
    "fiquei muito contente com o atendimento",
]

FRASES_NEGATIVAS = [
    "odiei o curso",
    "o professor explica muito mal",
    "a aula de hoje foi péssima",
    "não gostei da experiência",
    "produto de qualidade horrível",
    "atendimento lento e ineficiente",
    "ficou muito abaixo das minhas expectativas",
    "não recomendo para ninguém",
    "muito ruim, nunca mais volto",
    "a entrega atrasou semanas",
    "estou muito insatisfeito com o resultado",
    "pior compra que fiz este ano",
    "equipe grosseira e despreparada",
    "parou de funcionar no primeiro dia",
    "conteúdo confuso e desorganizado",
    "que experiência terrível",
    "detestei cada minuto",
    "não vale o preço cobrado",
    "simplesmente horrível",
    "fiquei decepcionado com a qualidade",
    "o suporte nunca responde",
    "interface feia e difícil de usar",
    "péssimo custo benefício",
    "nada funcionou como prometido",
    "o material da disciplina é fraco",
    "não aprendi nada nessa aula",
    "as atividades práticas foram um caos",
    "nota zero, cheio de defeitos",
    "chegou quebrado e mal embalado",
    "o serviço piorou muito ultimamente",
    "estou arrependido dessa compra",
    "a plataforma é lenta e instável",
    "didática ruim e exemplos confusos",
    "me senti muito mal atendido",
    "essa ferramenta atrapalhou meu trabalho",
    "resultado lamentável, que vergonha",
    "muito complicado e contraintuitivo",
    "a comida estava intragável",
    "ambiente sujo e bagunçado",
    "nunca mais compro nessa loja",
    "que aula entediante",
    "o laboratório foi mal conduzido",
    "não gostei do ritmo nem da falta de clareza",
    "tudo péssimo do começo ao fim",
    "experiência negativa em todos os sentidos",
    "o aplicativo trava toda hora",
    "não cumpriu nada do que prometeu",
    "estou muito frustrado com a escolha",
    "serviço deplorável",
    "foi a pior decisão que tomei",
    "o time foi muito rude comigo",
    "a qualidade do som é horrorosa",
    "documentação incompleta e desatualizada",
    "instalação complicada e cheia de erros",
    "desempenho muito abaixo do esperado",
    "a nova versão ficou pior",
    "muito ineficiente, desperdiçou meu tempo",
    "as explicações foram vagas e confusas",
    "produto frágil e mal construído",
    "fiquei irritado com o atendimento",
]

textos = FRASES_POSITIVAS + FRASES_NEGATIVAS
rotulos = ["positivo"] * len(FRASES_POSITIVAS) + ["negativo"] * len(FRASES_NEGATIVAS)

# ---------------------------------------------------------------------------
# Pipeline: vetorização TF-IDF (palavras e pares de palavras) + classificador
# ---------------------------------------------------------------------------

modelo = Pipeline(
    [
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000, C=50)),
    ]
)

# Validação cruzada rápida, só para termos uma noção da qualidade
scores = cross_val_score(modelo, textos, rotulos, cv=5)
print(f"Acurácia média (validação cruzada 5-fold): {scores.mean():.2%}")

# Treina com todos os dados e salva
modelo.fit(textos, rotulos)
joblib.dump(modelo, "modelo.pkl")
print(f"Modelo treinado com {len(textos)} frases e salvo em modelo.pkl")
