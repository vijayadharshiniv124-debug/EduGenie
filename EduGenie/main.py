from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", version="1.0.0", description="Google Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000)


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=10000)
    count: int = Field(default=5, ge=1, le=10)


class LearningRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field(default="beginner", min_length=1, max_length=50)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "EduGenie"}


def handle(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"EduGenie error: {exc}") from exc


@app.post("/qa")
def qa(payload: TextRequest):
    return {"answer": handle(answer_question, payload.text)}


@app.post("/explain")
def explain(payload: TextRequest):
    result = handle(explain_topic, payload.text)
    return {"explanation": result}


@app.post("/quiz")
def quiz(payload: QuizRequest):
    return {"quiz": handle(generate_quiz, payload.topic, payload.count)}


@app.post("/summarize")
def summarize(payload: TextRequest):
    return {"summary": handle(summarize_text, payload.text)}


@app.post("/learn/recommendations")
def learning(payload: LearningRequest):
    return {"recommendations": handle(recommend_learning_path, payload.topic, payload.level)}


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
