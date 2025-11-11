from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _register_login_and_shop():
    email = f"kpi_{uuid4().hex[:8]}@example.com"
    password = "ChangeMe123"

    # Register
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text

    # Login
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # Shop
    r = client.post(
        "/shops",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": f"KPI Shop {uuid4().hex[:4]}"},
    )
    assert r.status_code == 201, r.text
    shop_id = r.json()["id"]

    return token, shop_id


def test_kpis_aggregates_receipts_and_top_skus():
    token, shop_id = _register_login_and_shop()

    headers = {"Authorization": f"Bearer {token}"}

    # Create two receipts
    r1 = client.post(
        f"/shops/{shop_id}/receipts",
        headers=headers,
        json={"lines": [{"sku": "COCA-500", "qty": 2, "unit_price": 1.2}]},
    )
    assert r1.status_code == 201, r1.text

    r2 = client.post(
        f"/shops/{shop_id}/receipts",
        headers=headers,
        json={"lines": [{"sku": "AGUA-0500", "qty": 1, "unit_price": 1.0}]},
    )
    assert r2.status_code == 201, r2.text

    # Request KPIs
    rk = client.get(
        f"/shops/{shop_id}/kpis",
        headers=headers,
    )
    assert rk.status_code == 200, rk.text
    data = rk.json()

    assert data["shop_id"] == shop_id
    assert data["total_receipts"] == 2
    assert abs(data["total_revenue"] - 3.4) < 1e-6

    # Check that COCA-500 appears in top_skus
    skus = {item["sku"]: item for item in data["top_skus"]}
    assert "COCA-500" in skus
    assert skus["COCA-500"]["qty"] == 2
