from core.query_engine import QueryEngine


def test_query_engine_contract() -> None:
    engine = QueryEngine()
    result = engine.run("What is Product X pricing trend in 2024?")

    assert result.answer
    assert result.retrieval_quality in {"low", "medium", "high"}
    assert result.failure_reason
    assert 0 <= result.confidence <= 1
    assert "overall_score" in result.debug
