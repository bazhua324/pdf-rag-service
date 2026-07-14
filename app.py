import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag.pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

state: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    state["pipeline"] = RAGPipeline()
    logger.info("RAG pipeline ready")
    yield
    state.clear()

app = FastAPI(title="AskMyDocs", version="0.0.1", lifespan=lifespan)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=100)

class Source(BaseModel):
    page: int
    snippet: str

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    pipeline = state.get("pipeline")
    if pipeline is None:
        raise HTTPException(status_code=503, detail="pipeline is not initialized")
    result = pipeline.ask(req.question)
    return AskResponse(**result)
