from typing import Any
from gemini_client import generate_json

QUIZ_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 4},
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}


def _validate(quiz: Any, count: int):
    if not isinstance(quiz, list):
        raise RuntimeError("Quiz response was not a list.")
    cleaned = []
    for item in quiz[:count]:
        if not isinstance(item, dict):
            continue
        options = item.get("options", [])
        if not isinstance(options, list) or len(options) != 4:
            continue
        if item.get("correct_answer") not in options:
            continue
        cleaned.append({
            "question": str(item.get("question", "")),
            "options": [str(x) for x in options],
            "correct_answer": str(item["correct_answer"]),
            "explanation": str(item.get("explanation", "")),
        })
    if len(cleaned) < count:
        raise RuntimeError(f"Gemini returned only {len(cleaned)} valid quiz questions out of {count} requested.")
    return cleaned


def generate_quiz(topic: str, count: int = 5):
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic for the quiz.")
    prompt = (
        f"Create {count} educational multiple-choice questions about: {topic}\n"
        "Each question must have exactly four distinct options and exactly one correct answer. "
        "Include a short explanation for the correct answer. Return only the requested structured data."
    )
    result = generate_json(prompt, QUIZ_SCHEMA)
    return _validate(result, count)
