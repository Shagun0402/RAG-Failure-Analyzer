from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_query_endpoint_returns_diagnostics() -> None:
    response = client.post("/query", json={"query": "What is Product X pricing trend in 2024?"})
    payload = response.json()

    assert response.status_code == 200
    assert "answer" in payload
    assert "retrieval_quality" in payload
    assert "failure_reason" in payload
    assert "confidence" in payload
    assert "debug" in payload
