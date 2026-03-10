# Desafio MBA Engenharia de Software com IA - Full Cycle

---

## 🚀 RAG Pipeline: Semantic Search CLI with LangChain & pgVector

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgVector-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

*(🇺🇸 English version below | 🇧🇷 Versão em português abaixo)*

---

### 📌 Overview
This repository contains a full **Retrieval-Augmented Generation (RAG)** pipeline developed as a technical challenge for the AI Software Engineering MBA (Full Cycle). The system ingests a PDF document and saves its information in a PostgreSQL database with the pgVector extension. It provides a Command Line Interface (CLI) for users to ask questions and receive answers based strictly on the PDF content.

### 🏗️ Tech Stack
- **Language:** Python
- **Framework:** LangChain
- **Database:** PostgreSQL + pgVector
- **Infrastructure:** Docker & Docker Compose

### ⚙️ How to Run

**1. Prerequisites**
- Docker Desktop installed and running.
- Python 3 installed.
- API Key from OpenAI or Google Gemini.

**2. Setup**
Clone the repository and set up your environment variables:
```bash
cp .env.example .env
```
*Note: Make sure to fill in your API keys and the exact PDF path in the `.env` file.*

**3. Start the Infrastructure**
Spin up the PostgreSQL database with the pgVector extension:
```bash
docker compose up -d
```

**4. Python Virtual Environment**
Create and activate your virtual environment, then install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**5. Data Ingestion**
Execute the ingestion script to read the PDF, generate embeddings, and store the vectors:
```bash
python src/ingest.py
```

**6. Start the CLI Chat**
Run the semantic search interface:
```bash
python src/chat.py
```

---

## 🇧🇷 Português

### 📌 Sobre o Projeto
Este repositório contém um pipeline completo de **Geração Aumentada por Recuperação (RAG)**, desenvolvido como um desafio técnico para o MBA em Engenharia de Software com IA (Full Cycle). O sistema ingere um documento PDF e salva suas informações em um banco de dados PostgreSQL com a extensão pgVector. Ele fornece uma Interface de Linha de Comando (CLI) para que os usuários façam perguntas e recebam respostas baseadas estritamente no conteúdo do PDF.

### 🏗️ Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework:** LangChain
- **Banco de Dados:** PostgreSQL + pgVector
- **Infraestrutura:** Docker & Docker Compose

### ⚙️ Como Executar

**1. Pré-requisitos**
- Docker Desktop instalado e rodando.
- Python 3 instalado.
- Chave de API da OpenAI ou Google Gemini.

**2. Configuração Inicial**
Clone o repositório e configure suas variáveis de ambiente:
```bash
cp .env.example .env
```
*Nota: Não se esqueça de preencher suas chaves de API e o nome do PDF no arquivo `.env`.*

**3. Subir a Infraestrutura**
Inicie o banco de dados PostgreSQL com pgVector via Docker:
```bash
docker compose up -d
```

**4. Ambiente Virtual Python**
Crie e ative o ambiente virtual, e instale as dependências:
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**5. Ingestão de Dados**
Execute a ingestão do PDF para fatiar o texto, gerar os embeddings e salvar no banco de dados:
```bash
python src/ingest.py
```

**6. Iniciar o Chat CLI**
Rode a interface interativa de busca semântica para fazer suas perguntas:
```bash
python src/chat.py
```