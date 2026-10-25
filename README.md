# Regulatory Circular Compliance Agent

A runnable starter implementation for ingesting regulatory circular text, retrieving relevant passages, and generating policy-mapping drafts. It includes a local keyword/vector-style fallback so the API can be explored without cloud credentials. OpenAI and Pinecone integrations are optional adapters.

## Features
- FastAPI endpoints for health, circular ingestion, and compliance Q&A
- PostgreSQL-ready schema (SQLAlchemy) for circular metadata and review records
- Chunking + retrieval pipeline; optional OpenAI embeddings/chat and Pinecone
- Source snippets returned with answers to support analyst review
- Dockerfile and sample data

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

For the local demo, no API keys are required. Set `OPENAI_API_KEY`, `PINECONE_API_KEY`, and `DATABASE_URL` to enable configured integrations. The included retrieval fallback is intentionally lightweight and is not a substitute for a production vector database or legal/compliance review.

## Endpoints
- `GET /health`
- `POST /circulars/ingest` with `{"title":"...","regulator":"RBI","text":"..."}`
- `POST /compliance/ask` with `{"question":"...","policy_context":"..."}`

## Important
This is an educational starter project, not a certified compliance system. Verify all regulatory interpretations with qualified compliance professionals. Do not upload confidential documents to third-party services without approval.
