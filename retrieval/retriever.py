from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    source_id: str
    year: int
    score: float


class Retriever:
    """Simple lexical retriever for deterministic local development."""

    def __init__(self) -> None:
        self._corpus: list[tuple[str, str, int]] = [
            (
                "Product X pricing increased during 2024 due to supply chain pressure.",
                "market-report-q4",
                2024,
            ),
            (
                "In early 2025, Product X pricing stabilized as logistics costs dropped.",
                "market-report-q1",
                2025,
            ),
            (
                "A market analysis noted uneven demand across regions for Product X.",
                "regional-demand-brief",
                2023,
            ),
        ]

    def retrieve(self, query: str, k: int = 3) -> list[RetrievedChunk]:
        query_tokens = self._tokenize(query)
        scored_chunks: list[RetrievedChunk] = []

        for text, source_id, year in self._corpus:
            chunk_tokens = self._tokenize(text)
            overlap = len(query_tokens & chunk_tokens)
            denom = max(len(query_tokens | chunk_tokens), 1)
            score = round(overlap / denom, 3)
            scored_chunks.append(RetrievedChunk(text=text, source_id=source_id, year=year, score=score))

        scored_chunks.sort(key=lambda chunk: chunk.score, reverse=True)
        return scored_chunks[:k]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
        return {token for token in cleaned.split() if token}
