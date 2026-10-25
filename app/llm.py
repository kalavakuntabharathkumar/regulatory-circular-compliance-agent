import os
from .store import retrieve

def answer_question(question: str, policy_context: str = "") -> dict:
    matches = retrieve(question)
    sources = [
        {"circular_id": c.circular_id, "title": c.title, "regulator": c.regulator,
         "text": c.text, "score": round(score, 3)}
        for c, score in matches
    ]
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and sources:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            context = "\n\n".join(f"[{s['title']} | {s['circular_id']}] {s['text']}" for s in sources)
            prompt = (
                "You are a cautious compliance research assistant. Use only the supplied context. "
                "Distinguish explicit requirements from interpretation, cite source titles, and state uncertainty. "
                "Never claim to provide legal advice. If context is insufficient, say so.\n\n"
                f"Regulatory excerpts:\n{context}\n\nInternal policy context:\n{policy_context}\n\n"
                f"Question: {question}"
            )
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "system", "content": "Be precise and conservative."},
                          {"role": "user", "content": prompt}],
                temperature=0.1,
            )
            answer = response.choices[0].message.content or "No answer returned."
            return {"answer": answer, "sources": sources, "requires_human_review": True}
        except Exception as exc:
            fallback_note = f" OpenAI integration unavailable ({type(exc).__name__}); using extractive fallback."
    else:
        fallback_note = ""
    if not sources:
        answer = "I could not find a matching circular in the current index. Ingest relevant circular text and retry."
    else:
        answer = (
            "Potentially relevant excerpts were retrieved. Compare the cited language with the internal policy, "
            "identify applicable obligations, owners, evidence, and deadlines, and have a compliance analyst approve "
            "the interpretation. This demo fallback does not independently determine regulatory applicability."
            + fallback_note
        )
    return {"answer": answer, "sources": sources, "requires_human_review": True}
