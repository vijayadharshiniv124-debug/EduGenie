import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
# The original project document names Gemini 1.5 Pro. That legacy model is no longer a safe default.
# Keep the model configurable so the app can follow the currently available Gemini API model.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()
LOCAL_EXPLANATION_ENABLED = os.getenv("LOCAL_EXPLANATION_ENABLED", "false").lower() in {"1", "true", "yes"}
LOCAL_EXPLANATION_MODEL = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M").strip()
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "50000"))
