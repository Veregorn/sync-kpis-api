from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert data["info"].get("title") == "Sync KPIs API"


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
