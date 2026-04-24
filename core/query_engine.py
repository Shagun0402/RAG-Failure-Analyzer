from dataclasses import dataclass

from evaluation.failure_analyzer import FailureAnalyzer
from evaluation.retrieval_evaluator import RetrievalEvaluator
from retrieval.retriever import Retriever


@dataclass
class QueryEngineResult:
    answer: str
    retrieval_quality: str
    failure_reason: str
    confidence: float
    retrieved_chunks: list[str]
    debug: dict[str, float]


class QueryEngine:
    """Coordinates retrieval, evaluation, and failure analysis."""

    def __init__(self) -> None:
        self._retriever = Retriever()
        self._evaluator = RetrievalEvaluator()
        self._failure_analyzer = FailureAnalyzer()

    def run(self, query: str) -> QueryEngineResult:
        chunks = self._retriever.retrieve(query)
        metrics = self._evaluator.evaluate(query=query, retrieved_chunks=chunks)
        retrieval_quality, failure_reason, confidence = self._failure_analyzer.analyze(
            metrics=metrics,
            had_retrieval=bool(chunks),
        )

        if retrieval_quality == "high":
            answer = "Retrieved evidence is consistent enough for a grounded answer."
        elif retrieval_quality == "medium":
            answer = "Retrieved evidence is partial; review sources before relying on this answer."
        else:
            answer = "Insufficient evidence for a trustworthy answer."

        return QueryEngineResult(
            answer=answer,
            retrieval_quality=retrieval_quality,
            failure_reason=failure_reason,
            confidence=confidence,
            retrieved_chunks=[chunk.text for chunk in chunks],
            debug={
                "similarity_score": metrics.similarity_score,
                "entity_coverage": metrics.entity_coverage,
                "freshness_score": metrics.freshness_score,
                "diversity_score": metrics.diversity_score,
                "overall_score": metrics.overall_score,
            },
        )
