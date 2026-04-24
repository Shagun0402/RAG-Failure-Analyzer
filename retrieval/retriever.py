class Retriever:
    """Stub retriever used to bootstrap end-to-end API behavior."""

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        corpus = [
            "Product X pricing increased during 2024 due to supply chain pressure.",
            "In early 2025, Product X pricing stabilized as logistics costs dropped.",
            "A market analysis noted uneven demand across regions for Product X.",
        ]
        query_words = {word.lower() for word in query.split()}
        scored = sorted(
            corpus,
            key=lambda chunk: sum(token in chunk.lower() for token in query_words),
            reverse=True,
        )
        return scored[:k]
