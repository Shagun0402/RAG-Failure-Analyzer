from fastapi import FastAPI

from api.schemas import DebugMetrics, QueryRequest, QueryResponse
from core.query_engine import QueryEngine


def create_app() -> FastAPI:
    app = FastAPI(title="RAG Failure Analyzer", version="0.2.1")
    engine = QueryEngine()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/query", response_model=QueryResponse)
    def query(payload: QueryRequest) -> QueryResponse:
        result = engine.run(payload.query)
        return QueryResponse(
            answer=result.answer,
            retrieval_quality=result.retrieval_quality,
            failure_reason=result.failure_reason,
            confidence=result.confidence,
            retrieved_chunks=result.retrieved_chunks,
            debug=DebugMetrics(**result.debug),
        )

    return app


app = create_app()
