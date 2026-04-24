from evaluation.retrieval_evaluator import RetrievalMetrics


class FailureAnalyzer:
    """Maps retrieval metrics to a failure category and confidence."""

    def analyze(
        self,
        metrics: RetrievalMetrics,
        had_retrieval: bool | None = None,
        retrieved_chunks: list[str] | None = None,
    ) -> tuple[str, str, float]:
        if had_retrieval is None:
            had_retrieval = bool(retrieved_chunks)

        if not had_retrieval:
            return "low", "no retrieval", 0.1

        if metrics.freshness_score < 0.45:
            return "low", "stale knowledge", 0.28

        if metrics.similarity_score < 0.35:
            return "low", "embedding mismatch", 0.3

        if metrics.entity_coverage < 0.45:
            return "medium", "missing context", 0.46

        if metrics.diversity_score < 0.6:
            return "medium", "noisy context", 0.51

        if metrics.overall_score < 0.65:
            return "medium", "partial support", 0.58

        return "high", "none", 0.84
