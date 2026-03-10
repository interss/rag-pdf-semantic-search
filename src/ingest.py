import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

# 1. Loads variables from the .env file
# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Fetches dynamic settings from .env (Clean Code & Security)
# 2. Busca as configurações dinâmicas do .env (Clean Code & Segurança)
PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
MODELO_EMBEDDING = os.getenv("OPENAI_EMBEDDING_MODEL")

def ingest_pdf():
    """
    Main ingestion function: Reads the PDF, chunks it, and saves it to the vector database.
    Função principal de ingestão: Lê o PDF, fatia e salva no banco de dados vetorial.
    """
    print(f"Iniciando a ingestão do arquivo: {PDF_PATH}...")
    
    # Security validation: Checks if the file exists before attempting to open it
    # Validação de segurança: Verifica se o arquivo existe antes de tentar abrir
    if not os.path.exists(PDF_PATH):
        print(f"Erro: O arquivo {PDF_PATH} não foi encontrado na raiz do projeto.")
        return

    # 3. Loads the raw text from the PDF
    # 3. Carrega o texto bruto do PDF
    loader = PyPDFLoader(PDF_PATH)
    documentos = loader.load()

    # 4. Chunks the text (Split)
    # 4. Fatia o texto (Split)
    print("Fatiando o documento...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"O documento foi dividido em {len(chunks)} pedaços.")

    # 5. Configures the Embeddings model using the variable from .env
    # 5. Configura o modelo de Embeddings usando a variável do .env
    embeddings = OpenAIEmbeddings(model=MODELO_EMBEDDING)

    # 6. Saves to the Database with Idempotency
    # 6. Salva no Banco de Dados com Idempotência
    print("Vetorizando e salvando no PostgreSQL (pgVector)...")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
        # Clears the old vectors of the document before inserting the new ones
        # Limpa os vetores antigos do documento antes de inserir os novos
        pre_delete_collection=True 
    )
    
    vector_store.add_documents(chunks)
    print("Ingestão concluída com sucesso! Vetores atualizados no banco de forma limpa.")

if __name__ == "__main__":
    ingest_pdf()