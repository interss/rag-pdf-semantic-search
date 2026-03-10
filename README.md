# Desafio MBA Engenharia de Software com IA - Full Cycle

Descreva abaixo como executar a sua solução.

---

## 🚀 RAG Pipeline: Semantic Search CLI with LangChain & pgVector

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgVector-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

*(🇺🇸 English version below | 🇧🇷 Versão em português abaixo)*

---

## 🇺🇸 English

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
*Note: Make sure to open the generated `.env` file and fill in your `OPENAI_API_KEY`. (The PDF path and local database credentials should already be filled by default).*

**3. Start the Infrastructure**
Spin up the PostgreSQL database with the pgVector extension locally:
```bash
docker compose up -d
```

**4. Python Virtual Environment**
Create the virtual environment to isolate the project's libraries:
```bash
python3 -m venv venv
```

Activate the virtual environment:
* **Linux/Mac/WSL:**
  ```bash
  source venv/bin/activate
  ```
* **Windows (PowerShell/CMD):**
  ```bash
  venv\Scripts\activate
  ```

With the environment activated, upgrade pip and install the dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**5. Data Ingestion**
Execute the ingestion script to read the PDF, generate embeddings, and store the vectors in the database:
```bash
python src/ingest.py
```

**6. Start the CLI Chat**
Run the interactive semantic search interface in your terminal to ask questions:
```bash
python src/chat.py
```

---

## 🇧🇷 Português

### 📌 Sobre o Projeto
Este repositório contém um pipeline completo de Geração Aumentada por Recuperação (RAG) desenvolvido como um desafio técnico para o MBA em Engenharia de Software com Inteligência Artificial (Full Cycle). O sistema ingere um documento PDF e salva suas informações em um banco de dados PostgreSQL com a extensão pgVector. Ele fornece uma Interface de Linha de Comando (CLI) para que os usuários façam perguntas e recebam respostas baseadas estritamente no conteúdo do PDF.

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
*Nota: Abra o arquivo `.env` gerado e preencha a sua `OPENAI_API_KEY`. (O caminho do PDF e as credenciais locais do banco de dados já devem vir preenchidas por padrão no arquivo).*

**3. Subir a Infraestrutura**
Inicie o banco de dados PostgreSQL com a extensão pgVector localmente:
```bash
docker compose up -d
```

**4. Ambiente Virtual Python**
Crie o ambiente virtual para isolar as bibliotecas do projeto:
```bash
python3 -m venv venv
```

Ative o ambiente virtual:
* **No Linux/Mac/WSL:**
  ```bash
  source venv/bin/activate
  ```
* **No Windows (PowerShell/CMD):**
  ```bash
  venv\Scripts\activate
  ```

Com o ambiente ativado, atualize o instalador e baixe as dependências:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**5. Ingestão de Dados**
Execute o script de ingestão. Ele lerá o PDF, fatiará o texto, gerará os embeddings na OpenAI e salvará os vetores no banco de dados:
```bash
python src/ingest.py
```

**6. Iniciar o Chat CLI**
Rode a interface interativa no terminal para fazer perguntas sobre o documento:
```bash
python src/chat.py
```