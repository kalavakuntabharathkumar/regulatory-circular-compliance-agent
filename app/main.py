from fastapi import FastAPI, HTTPException
from .schemas import IngestRequest, AskRequest
from .store import add_circular
from .llm import answer_question

app = FastAPI(title="Regulatory Circular Compliance Agent", version="0.1.0",
              description="Compliance research prototype. Human review is required.")

@app.get("/health")
def health():
    return {"status": "ok", "service": "regulatory-compliance-agent"}

@app.post("/circulars/ingest")
def ingest(request: IngestRequest):
    result = add_circular(request.title, request.regulator, request.text, request.circular_id)
    return {"status": "ingested", **result}

@app.post("/compliance/ask")
def ask(request: AskRequest):
    result = answer_question(request.question, request.policy_context)
    if not result["sources"]:
        # Return a useful response rather than treating no retrieval as an API failure.
        return result
    return result
