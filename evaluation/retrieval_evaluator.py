from dataclasses import dataclass


@dataclass
class RetrievalMetrics:
    similarity_score: float
    entity_coverage: float
    freshness_score: float
    diversity_score: float


class RetrievalEvaluator:
    """Heuristic retrieval evaluator used as the first implementation milestone."""

    def evaluate(self, query: str, retrieved_chunks: list[str]) -> RetrievalMetrics:
        if not retrieved_chunks:
            return RetrievalMetrics(
                similarity_score=0.0,
                entity_coverage=0.0,
                freshness_score=0.0,
                diversity_score=0.0,
            )

        query_terms = {token.lower() for token in query.split() if token.strip()}
        chunk_text = " ".join(retrieved_chunks).lower()
        chunk_terms = {token for token in chunk_text.split() if token.strip()}

        overlap = len(query_terms & chunk_terms)
        similarity_score = overlap / max(len(query_terms), 1)

        capitalized_entities = [token for token in query.split() if token[:1].isupper()]
        if capitalized_entities:
            covered = sum(1 for entity in capitalized_entities if entity.lower() in chunk_text)
            entity_coverage = covered / len(capitalized_entities)
        else:
            entity_coverage = min(similarity_score + 0.2, 1.0)

        freshness_score = 0.4
        if any(str(year) in chunk_text for year in (2024, 2025, 2026)):
            freshness_score = 0.8

        unique_chunks = len(set(chunk.lower().strip() for chunk in retrieved_chunks))
        diversity_score = unique_chunks / len(retrieved_chunks)

        return RetrievalMetrics(
            similarity_score=round(similarity_score, 2),
            entity_coverage=round(entity_coverage, 2),
            freshness_score=round(freshness_score, 2),
            diversity_score=round(diversity_score, 2),
        )
