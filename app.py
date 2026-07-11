from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="AskMyDocs", version="0.0.1")

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
    source: list[Source]

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return AskResponse(
        answer=f"You asked: {request.question}",
        source=[Source(page=1, snippet= "placeholder")])