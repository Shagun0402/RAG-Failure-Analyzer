from evaluation.retrieval_evaluator import RetrievalMetrics


class FailureAnalyzer:
    """Maps retrieval metrics to a user-facing failure reason and confidence."""

    def analyze(self, metrics: RetrievalMetrics, retrieved_chunks: list[str]) -> tuple[str, str, float]:
        if not retrieved_chunks:
            return "low", "no retrieval", 0.1

        if metrics.freshness_score < 0.5:
            return "low", "stale knowledge", 0.33

        if metrics.similarity_score < 0.35:
            return "low", "embedding mismatch", 0.3

        if metrics.entity_coverage < 0.4:
            return "medium", "missing context", 0.45

        if metrics.diversity_score < 0.5:
            return "medium", "noisy context", 0.5

        return "high", "none", 0.82
