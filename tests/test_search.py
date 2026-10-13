import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from search import search_prompt  # noqa: E402

REFUSAL = "Não tenho informações necessárias para responder sua pergunta."


def test_prompt_contains_context_and_question():
    prompt = search_prompt("Qual o faturamento?", retriever=lambda q: "Alfa S.A. R$ 10")
    assert "Alfa S.A. R$ 10" in prompt
    assert "Qual o faturamento?" in prompt


def test_prompt_keeps_refusal_rule():
    prompt = search_prompt("Capital da França?", retriever=lambda q: "")
    assert REFUSAL in prompt


def test_empty_question_skips_retrieval():
    def fail(_question):
        raise AssertionError("retriever must not be called")

    assert search_prompt("", retriever=fail) == "No question provided."
