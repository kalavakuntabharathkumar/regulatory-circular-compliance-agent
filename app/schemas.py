from pydantic import BaseModel, Field

class IngestRequest(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    regulator: str = Field(default="RBI", max_length=30)
    circular_id: str | None = None
    text: str = Field(min_length=20)

class AskRequest(BaseModel):
    question: str = Field(min_length=5)
    policy_context: str = ""

class SourceChunk(BaseModel):
    circular_id: str
    title: str
    regulator: str
    text: str
    score: float

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    requires_human_review: bool = True
