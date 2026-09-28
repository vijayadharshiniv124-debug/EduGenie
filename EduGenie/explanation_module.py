from config import LOCAL_EXPLANATION_ENABLED, LOCAL_EXPLANATION_MODEL
from gemini_client import generate_text

_local_pipeline = None


def _get_local_pipeline():
    global _local_pipeline
    if _local_pipeline is None:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError("Local explanation dependencies are not installed. Install requirements-local.txt or disable LOCAL_EXPLANATION_ENABLED.") from exc
        _local_pipeline = pipeline("text2text-generation", model=LOCAL_EXPLANATION_MODEL)
    return _local_pipeline


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic to explain.")

    if LOCAL_EXPLANATION_ENABLED:
        try:
            generator = _get_local_pipeline()
            prompt = f"Explain the following educational topic simply for a beginner. Use short sentences and a small example when useful. Topic: {topic}"
            result = generator(prompt, max_new_tokens=180, do_sample=False)[0]["generated_text"]
            if result.strip():
                return result.strip()
        except Exception:
            # Cloud fallback keeps the application usable when the local model is unavailable.
            pass

    return generate_text(
        "Explain the following educational topic in simple language for a beginner. "
        "Be concise, clear, and use a short example if helpful. Do not assume prior knowledge.\n\n"
        f"Topic: {topic}"
    )
