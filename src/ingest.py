import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

# Settings come from .env so no secret or path is hardcoded.
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")


def ingest_pdf():
    """Read the PDF, split it into chunks and store their embeddings in pgVector."""
    print(f"Ingesting {PDF_PATH}...")

    if not os.path.exists(PDF_PATH):
        print(f"Error: {PDF_PATH} not found in the project root.")
        return

    documents = PyPDFLoader(PDF_PATH).load()

    print("Splitting the document...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    print("Embedding and saving to PostgreSQL (pgVector)...")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
        # Idempotent: drop the previous vectors so re-running never duplicates chunks.
        pre_delete_collection=True,
    )

    vector_store.add_documents(chunks)
    print("Ingestion complete.")


if __name__ == "__main__":
    ingest_pdf()
