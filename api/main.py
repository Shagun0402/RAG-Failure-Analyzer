from fastapi import FastAPI

from api.schemas import DebugMetrics, QueryRequest, QueryResponse
from evaluation.failure_analyzer import FailureAnalyzer
from evaluation.retrieval_evaluator import RetrievalEvaluator
from retrieval.retriever import Retriever

app = FastAPI(title="RAG Failure Analyzer", version="0.1.0")

retriever = Retriever()
evaluator = RetrievalEvaluator()
failure_analyzer = FailureAnalyzer()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    retrieved_chunks = retriever.retrieve(payload.query)
    metrics = evaluator.evaluate(payload.query, retrieved_chunks)
    retrieval_quality, failure_reason, confidence = failure_analyzer.analyze(metrics, retrieved_chunks)

    if retrieval_quality == "high":
        answer = "Based on retrieved evidence, the trend appears stable with periodic changes."
    else:
        answer = "Insufficient evidence for a high-confidence answer."

    return QueryResponse(
        answer=answer,
        retrieval_quality=retrieval_quality,
        failure_reason=failure_reason,
        confidence=confidence,
        retrieved_chunks=retrieved_chunks,
        debug=DebugMetrics(
            similarity_score=metrics.similarity_score,
            entity_coverage=metrics.entity_coverage,
            freshness_score=metrics.freshness_score,
            diversity_score=metrics.diversity_score,
        ),
    )
