from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, description="User query to analyze")


class DebugMetrics(BaseModel):
    similarity_score: float
    entity_coverage: float
    freshness_score: float
    diversity_score: float


class QueryResponse(BaseModel):
    answer: str
    retrieval_quality: str
    failure_reason: str
    confidence: float
    retrieved_chunks: list[str]
    debug: DebugMetrics
