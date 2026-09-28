# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant built around FastAPI and a simple HTML/CSS frontend. It supports:

- Q&A
- Simplified topic explanations
- Multiple-choice quiz generation
- Educational summarization
- Personalized learning recommendations

The project follows the architecture described in the supplied project document: `main.py`, `explanation_module.py`, `qna.py`, `quiz_module.py`, `summary_module.py`, `learning_path.py`, `templates/index.html`, and `static/style.css`.

## Important model note

The supplied document specifies **Gemini 1.5 Pro** for Q&A, summarization, quiz generation, and learning paths, and **LaMini-Flan-T5-783M** for concept explanation. Gemini 1.5 Pro is no longer a safe/current API default, so this implementation makes the Gemini model configurable with `GEMINI_MODEL`. The default is a current Gemini model; you can change it without editing Python code.

## 1. Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10+
- A Gemini API key
- VS Code (recommended)

## 2. Create the environment

Windows PowerShell:

```powershell
cd path\to\EduGenie
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and put your key in:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-3.6-flash
```

Never commit `.env` or share the API key.

## 4. Run

```powershell
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

FastAPI's interactive API documentation is at `http://127.0.0.1:8000/docs`.

## 5. Test

In a second terminal, with the virtual environment active:

```powershell
pytest -q
```

The included tests verify the homepage, health endpoint, and request validation without calling Gemini.

## 6. Optional local explanation model

The project document describes LaMini-Flan-T5-783M as the local explanation model. To enable it:

```powershell
pip install -r requirements-local.txt
```

Then set:

```env
LOCAL_EXPLANATION_ENABLED=true
```

The model is downloaded the first time it is used and can require substantial RAM/disk. If local inference fails, EduGenie automatically falls back to Gemini so the explanation feature remains usable.

## API endpoints

- `GET /` — frontend
- `GET /health` — health check
- `POST /qa` — answer a question
- `POST /explain` — explain a topic simply
- `POST /quiz` — generate a structured MCQ quiz
- `POST /summarize` — summarize an educational passage
- `POST /learn/recommendations` — generate a learning path

Example Q&A request:

```json
{"text":"Which is the largest ocean?"}
```

Example quiz request:

```json
{"topic":"Pythagoras theorem","count":5}
```

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Make sure `.env` exists in the project root and contains a valid key.

### `404 NOT_FOUND` for a Gemini model
Change `GEMINI_MODEL` in `.env` to a currently available model. The application intentionally does not hard-code the legacy Gemini 1.5 Pro name.

### `503 UNAVAILABLE`
This usually means the selected model/service is temporarily unavailable or rate-limited. Try again later or select another currently available model in `.env`.

### `getaddrinfo failed`
This is a network/DNS problem. Check your internet connection, VPN/proxy, and DNS settings, then retry.

### Local model is slow or runs out of memory
Set `LOCAL_EXPLANATION_ENABLED=false` and use Gemini for explanations, or install the local model only on a machine with sufficient RAM.
