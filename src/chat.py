import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_prompt

load_dotenv()

LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano")
EXIT_COMMANDS = {"exit", "quit", "sair"}


def main():
    """Start the LLM and run the question/answer loop in the terminal."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Configuration error: OPENAI_API_KEY not found in .env")
        return

    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    print("=" * 60)
    print("RAG document assistant")
    print("Ask a question about the document, or type 'exit' to quit.")
    print("=" * 60)

    while True:
        question = input("\nQUESTION: ")
        if question.strip().lower() in EXIT_COMMANDS:
            print("Bye.")
            break
        if not question.strip():
            continue

        try:
            answer = llm.invoke(search_prompt(question))
            print(f"ANSWER: {answer.content}")
        except Exception as e:
            print(f"\n[LLM or database error]: {e}")


if __name__ == "__main__":
    main()
