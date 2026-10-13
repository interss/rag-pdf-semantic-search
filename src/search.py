import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
TOP_K = 10

# The prompt stays in Portuguese on purpose: the source PDF is in Portuguese and the
# challenge specifies the exact refusal sentence for out-of-context questions.
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


def retrieve_context(question):
    """Return the TOP_K chunks most similar to the question, joined as one string."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )
    results = vector_store.similarity_search_with_score(question, k=TOP_K)
    return "\n\n".join(document.page_content for document, _score in results)


def search_prompt(question, retriever=retrieve_context):
    """Build the final prompt: retrieved context plus the user's question."""
    if not question:
        return "No question provided."

    return PROMPT_TEMPLATE.format(
        contexto=retriever(question),
        pergunta=question,
    )


if __name__ == "__main__":
    print(search_prompt("Qual é o faturamento da empresa?"))
