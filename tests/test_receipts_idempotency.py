from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _register_and_login() -> str:
    email = f"m2_{uuid4().hex[:8]}@example.com"
    password = "ChangeMe123"

    # Register
    r = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert r.status_code == 201, r.text

    # Login
    r = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    return data["access_token"]


def _create_shop(token: str) -> int:
    r = client.post(
        "/shops",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": f"Shop-{uuid4().hex[:4]}"},
    )
    assert r.status_code == 201, r.text
    data = r.json()
    return data["id"]


def test_receipt_idempotency_same_key_returns_same_receipt() -> None:
    token = _register_and_login()
    shop_id = _create_shop(token)

    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "idem-test-123",
    }
    body = {
        "lines": [
            {"sku": "COCA-500", "qty": 2, "unit_price": 1.2},
        ]
    }

    # First request
    r1 = client.post(
        f"/shops/{shop_id}/receipts",
        headers=headers,
        json=body,
    )
    assert r1.status_code == 201, r1.text
    data1 = r1.json()
    assert "id" in data1
    assert data1["total"] == 2.4

    # Second request with same Idempotency-Key and same body
    r2 = client.post(
        f"/shops/{shop_id}/receipts",
        headers=headers,
        json=body,
    )
    assert r2.status_code == 201, r2.text
    data2 = r2.json()

    # Should return the same receipt (idempotency)
    assert data2["id"] == data1["id"]
    assert data2["total"] == data1["total"]
