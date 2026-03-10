import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

# 1. Load environment variables
# 1. Carregar variáveis de ambiente
load_dotenv()

# 2. Fetching dynamic settings from .env (Security and Scalability)
# 2. Buscando configurações dinâmicas do .env (Segurança e Escalabilidade)
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
MODELO_EMBEDDING = os.getenv("OPENAI_EMBEDDING_MODEL")

# 3. The Mandatory Template for the Challenge
# 3. O Template Obrigatório do Desafio
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def realizar_busca(pergunta):
    """
    Goes to the database and retrieves the relevant text chunks.
    Vai até o banco de dados e traz os pedaços de texto relevantes.
    """
    # Model comes from .env!
    # Modelo vem do .env!
    embeddings = OpenAIEmbeddings(model=MODELO_EMBEDDING)
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True
    )
    
    # Searches for the 10 most relevant results
    # Busca os 10 resultados mais relevantes
    resultados = vector_store.similarity_search_with_score(pergunta, k=10)
    
    textos_recuperados = []
    for documento, score in resultados:
        textos_recuperados.append(documento.page_content)
        
    return "\n\n".join(textos_recuperados)

def search_prompt(question):
    """
    Fetches the context and formats the PROMPT_TEMPLATE.
    Busca o contexto e formata o PROMPT_TEMPLATE.
    """
    if not question:
        return "Nenhuma pergunta foi fornecida."
        
    # 1. Hunts for the context in the database
    # 1. Caça o contexto no banco
    contexto_encontrado = realizar_busca(question)
    
    # 2. Injects the context and the question into the Template
    # 2. Injeta o contexto e a pergunta no Template
    prompt_final = PROMPT_TEMPLATE.format(
        contexto=contexto_encontrado,
        pergunta=question
    )
    
    return prompt_final

if __name__ == "__main__":
    teste = search_prompt("Qual é o faturamento da empresa?")
    print("\n=== PROMPT GERADO PRONTO PARA A IA ===")
    print(teste)