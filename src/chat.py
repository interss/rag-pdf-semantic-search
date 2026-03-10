import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Imports search function
# Importa função de busca
from search import search_prompt

# 1. Loads environment variables
# 1. Carrega variáveis de ambiente
load_dotenv()

# 2. LLM Model configuration required by the Challenge
# 2. Configuração do Modelo LLM exigido pelo Desafio
MODELO_LLM = os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano")

def main():
    """
    Main function that initializes the AI and keeps the chat loop running.
    Função principal que inicializa a IA e mantém o loop do chat rodando.
    """
    # Initial Validation (Replaces the 'chain = search_prompt()' logic)
    # Validação Inicial (Substitui a lógica de 'chain = search_prompt()')
    # Ensures that the OpenAI key exists before starting the chat
    # Garanti que a chave da OpenAI existe antes de iniciar o chat
    try:
        # temperature=0 for the AI to focus only on the PDF
        # temperature=0 para a IA focar apenas no PDF
        llm = ChatOpenAI(model=MODELO_LLM, temperature=0)
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("API Key da OpenAI não encontrada no .env")
        chat_pronto = True
    except Exception as e:
        print(f"Erro de configuração: {e}")
        chat_pronto = False

    # Security check
    # Verificação de segurança
    if not chat_pronto:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    # === INTERACTIVE LOOP ===
    # === LOOP INTERATIVO ===
    print("="*60)
    print("🤖 Assistente RAG de Documentos")
    print("Digite sua pergunta ou digite 'sair' para encerrar.")
    print("="*60)

    while True:
        # Receives the user's question in the terminal
        # Recebe a pergunta do usuário no terminal
        pergunta = input("\nPERGUNTA: ")
        
        # Condition to exit the program
        # Condição para sair do programa
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o sistema. Até logo!")
            break
            
        # Prevents the system from crashing if the user presses Enter with an empty line
        # Evita que o sistema quebre se o usuário der Enter com a linha vazia
        if not pergunta.strip():
            continue

        try:
            # 1. Triggers search.py to fetch from the database and build the prompt
            # 1. Aciona o search.py para buscar no banco e montar o prompt
            prompt_formatado = search_prompt(pergunta)

            # 2. Sends the prompt to the OpenAI gpt-5-nano model
            # 2. Envia o prompt para o modelo gpt-5-nano da OpenAI
            resposta_ia = llm.invoke(prompt_formatado)
            
            # 3. Prints the response
            # 3. Imprime a resposta
            print(f"RESPOSTA: {resposta_ia.content}")
            
        except Exception as e:
            print(f"\n[Erro na comunicação com a IA ou Banco]: {e}")

# Standard Python entry point
# Ponto de entrada padrão do Python
if __name__ == "__main__":
    main()