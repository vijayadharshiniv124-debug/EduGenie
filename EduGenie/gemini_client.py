from functools import lru_cache
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to the .env file.")
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_json(prompt: str, schema: dict):
    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    parsed = getattr(response, "parsed", None)
    if parsed is not None:
        return parsed
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no JSON content.")
    import json
    return json.loads(text)
