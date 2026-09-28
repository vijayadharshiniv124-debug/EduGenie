from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Please provide text to summarize.")
    return generate_text(
        "Summarize the following educational passage for quick revision. Preserve the main ideas, important facts, "
        "and relationships. Remove repetition. Use clear language and short paragraphs or bullets where useful.\n\n"
        f"Passage:\n{text}"
    )
