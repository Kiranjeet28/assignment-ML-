import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .agent import get_agent
from .utils import detect_plot_needed, generate_plot, log_user_query
from .data_loader import load_titanic_dataset

load_dotenv()

logging.basicConfig(level=logging.INFO)


# FIX: @app.on_event("startup") is deprecated in FastAPI.
# Use the modern `lifespan` context manager instead.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup ──────────────────────────────────────────────────────────────
    try:
        get_agent()
        logging.info("✅ Agent initialised and cached successfully.")
    except Exception:
        logging.error("❌ Agent failed to initialise:\n" + traceback.format_exc())

    yield  # application runs here

    # ── shutdown (add cleanup here if needed) ────────────────────────────────


app = FastAPI(title="Titanic Chat Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    text_answer: str
    plot_needed: bool
    plot_base64: str | None = None


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    question = request.question.strip()
    if len(question) < 3 or len(question) > 512:
        raise HTTPException(
            status_code=400,
            detail="Question length must be between 3 and 512 characters.",
        )
    try:
        # Out-of-context detection: Only answer Titanic-related questions
        titanic_keywords = [
            "titanic", "passenger", "survivor", "survived", "pclass", "fare", "embarked", "age", "sex", "sibsp", "parch", "cabin", "ticket"
        ]
        if not any(kw in question.lower() for kw in titanic_keywords):
            return AskResponse(
                text_answer="It's out of context",
                plot_needed=False,
                plot_base64=None,
            )

        agent = get_agent()

        # invoke() — agent.run() was deprecated in langchain 0.1.0
        result_dict = agent.invoke({"input": question})
        result = result_dict.get("output", "")

        plot_needed = detect_plot_needed(question) or ("plot" in result.lower())
        plot_base64 = None
        if plot_needed:
            df = load_titanic_dataset()
            plot_base64 = generate_plot(df, question)

        log_user_query(question, result)
        return AskResponse(
            text_answer=result,
            plot_needed=plot_needed,
            plot_base64=plot_base64,
        )
    except Exception:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.get("/health")
def health():
    return {"status": "ok"}