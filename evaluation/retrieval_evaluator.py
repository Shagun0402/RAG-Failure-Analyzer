from dataclasses import dataclass
from datetime import datetime, timezone

from retrieval.retriever import RetrievedChunk


@dataclass
class RetrievalMetrics:
    similarity_score: float
    entity_coverage: float
    freshness_score: float
    diversity_score: float
    overall_score: float


class RetrievalEvaluator:
    """Evaluates retrieved chunks using deterministic heuristics."""

    def evaluate(
        self,
        query: str,
        retrieved_chunks: list[RetrievedChunk],
        current_year: int | None = None,
    ) -> RetrievalMetrics:
        if not retrieved_chunks:
            return RetrievalMetrics(0.0, 0.0, 0.0, 0.0, 0.0)

        resolved_year = current_year or datetime.now(timezone.utc).year

        query_tokens = self._tokenize(query)
        combined_text = " ".join(chunk.text for chunk in retrieved_chunks)
        combined_tokens = self._tokenize(combined_text)

        similarity_score = len(query_tokens & combined_tokens) / max(len(query_tokens), 1)

        entities = [token for token in query.split() if token[:1].isupper()]
        if entities:
            entity_hits = sum(1 for entity in entities if entity.lower().strip("?.!,") in combined_text.lower())
            entity_coverage = entity_hits / len(entities)
        else:
            entity_coverage = similarity_score

        avg_age = sum(max(resolved_year - chunk.year, 0) for chunk in retrieved_chunks) / len(retrieved_chunks)
        freshness_score = max(0.0, 1 - (avg_age / 5))

        unique_sources = len({chunk.source_id for chunk in retrieved_chunks})
        diversity_score = unique_sources / len(retrieved_chunks)

        overall_score = (
            0.4 * similarity_score
            + 0.25 * entity_coverage
            + 0.2 * freshness_score
            + 0.15 * diversity_score
        )

        return RetrievalMetrics(
            similarity_score=round(similarity_score, 2),
            entity_coverage=round(entity_coverage, 2),
            freshness_score=round(freshness_score, 2),
            diversity_score=round(diversity_score, 2),
            overall_score=round(overall_score, 2),
        )

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
        return {token for token in cleaned.split() if token}
