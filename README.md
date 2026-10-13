# RAG PDF Semantic Search

**Ask questions about a PDF from the terminal and get answers grounded only in that
document.** A retrieval-augmented generation (RAG) pipeline built with LangChain,
PostgreSQL + pgVector and OpenAI.

Built as the ingestion-and-search challenge of the Full Cycle MBA in AI Software
Engineering. The starter template (Docker setup, sample PDF, file skeleton) is
[devfullcycle/mba-ia-desafio-ingestao-busca](https://github.com/devfullcycle/mba-ia-desafio-ingestao-busca);
the ingestion, retrieval, prompt and chat code are mine.

## How it works

1. **Ingest** (`src/ingest.py`): load the PDF, split it into 1,000-character chunks with
   150 characters of overlap, embed each chunk and store it in pgVector. Re-running is
   idempotent: the collection is cleared before inserting, so chunks never duplicate.
2. **Retrieve** (`src/search.py`): embed the question and fetch the 10 most similar chunks.
3. **Answer** (`src/chat.py`): send the retrieved context plus the question to the LLM with
   strict rules: answer only from the context, and reply with a fixed refusal sentence
   when the answer is not in the document.

The sample PDF is a fictional table of companies, revenues and founding years, in
Portuguese, so the prompt and the refusal sentence are in Portuguese too.

## Quickstart

Requires Docker, Python 3.12 or newer (tested on 3.12 and 3.14) and an OpenAI API key.

```bash
git clone https://github.com/interss/rag-pdf-semantic-search.git
cd rag-pdf-semantic-search
cp .env.example .env          # then set OPENAI_API_KEY; the other defaults already match docker-compose
docker compose up -d          # PostgreSQL 17 with the pgVector extension

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python src/ingest.py          # load the PDF into pgVector
python src/chat.py            # ask questions; type "exit" to quit
```

Expected behavior (illustrative, not a recorded run):

```
QUESTION: Qual o faturamento da Alfa Energia S.A.?
ANSWER: R$ 722.875.391,46.

QUESTION: Qual é a capital da França?
ANSWER: Não tenho informações necessárias para responder sua pergunta.
```

## Configuration

All settings live in `.env` (see [`.env.example`](.env.example)):

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | (empty) | Required |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `OPENAI_LLM_MODEL` | `gpt-5-nano` | Chat model |
| `DATABASE_URL` | local Docker database | pgVector connection string |
| `PG_VECTOR_COLLECTION_NAME` | `document_chunks` | Collection that stores the chunks |
| `PDF_PATH` | `document.pdf` | Document to ingest |

## Tests

The prompt-building logic is tested with a fake retriever, so no database, network or API
key is needed:

```bash
pip install pytest
python -m pytest
```

## Design choices

- **Grounded answers over helpful guesses.** The prompt forbids outside knowledge and
  opinions, with few-shot examples of questions that must be refused.
- **Idempotent ingestion.** `pre_delete_collection=True` makes re-ingesting safe.
- **No hardcoded secrets.** Keys and connection strings come from `.env`, which is
  git-ignored; the chat exits with a clear message when the key is missing.
- **Testable retrieval.** `search_prompt` accepts the retriever as a parameter, so the
  prompt can be tested without pgVector.

## Repository layout

```
.
├── src/
│   ├── ingest.py        PDF → chunks → embeddings → pgVector
│   ├── search.py        similarity search + prompt template
│   └── chat.py          interactive CLI
├── tests/               unit tests (no network)
├── document.pdf         sample document (from the challenge template)
├── docker-compose.yml   PostgreSQL + pgVector
├── requirements.txt
└── .env.example
```
