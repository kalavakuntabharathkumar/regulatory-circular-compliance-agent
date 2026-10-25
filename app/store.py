from dataclasses import dataclass
import re
from uuid import uuid4

@dataclass
class Chunk:
    circular_id: str
    title: str
    regulator: str
    text: str

_chunks: list[Chunk] = []

def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    clean = re.sub(r"\\s+", " ", text).strip()
    if not clean:
        return []
    out, start = [], 0
    while start < len(clean):
        end = min(len(clean), start + size)
        out.append(clean[start:end])
        if end == len(clean):
            break
        start = max(end - overlap, start + 1)
    return out

def add_circular(title: str, regulator: str, text: str, circular_id: str | None = None) -> dict:
    cid = circular_id or str(uuid4())
    pieces = chunk_text(text)
    for piece in pieces:
        _chunks.append(Chunk(cid, title, regulator.upper(), piece))
    return {"circular_id": cid, "chunks_added": len(pieces)}

def retrieve(question: str, limit: int = 4) -> list[tuple[Chunk, float]]:
    terms = {t.lower() for t in re.findall(r"[a-zA-Z0-9]{3,}", question)}
    scored = []
    for c in _chunks:
        words = {t.lower() for t in re.findall(r"[a-zA-Z0-9]{3,}", c.text)}
        score = len(terms & words) / max(len(terms), 1)
        if score:
            scored.append((c, score))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:limit]

def clear_store():
    _chunks.clear()
