from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")
    return generate_text(
        "You are EduGenie, a helpful academic assistant. Answer the student's question accurately and concisely. "
        "If the question is ambiguous, state the assumption you used. Prefer plain language and useful examples.\n\n"
        f"Question: {question}"
    )
