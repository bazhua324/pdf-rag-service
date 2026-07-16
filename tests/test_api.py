from fastapi.testclient import TestClient
import app as app_module
from app import app

class FakePipeline:
    def ask(self, question: str) -> dict:
        return {
            "answer": question,
            "sources": [{"page": 1, "snippet": "stub snippet"}]
        }

def make_client():
    app_module.state["pipeline"] = FakePipeline()
    return TestClient(app)

def test_health():
    client = make_client()
    r = client.get("/health")
    assert r.status_code == 200

def test_ask_returns_answer_and_sources():
    client = make_client()
    r = client.post("/ask", json={"question": "What's going on today?"})
    assert r.status_code == 200
    assert "answer" in r.json()

def test_ask_rejects_empty_question():
    client = make_client()
    r = client.post("/ask", json={"question": ""})
    assert r.status_code == 422
