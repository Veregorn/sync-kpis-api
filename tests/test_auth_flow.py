from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login_and_create_shop() -> None:
    # Unique email to avoid collision if the test is executed multiple times
    email = f"test_{uuid4().hex[:8]}@example.com"
    password = "ChangeMe123"

    # 1) Register
    r = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert "access_token" in data

    # 2) Login
    r = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    login_data = r.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # 3) Create shop
    r = client.post(
        "/shops",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Shop"},
    )
    assert r.status_code == 201, r.text
    shop = r.json()
    assert shop["name"] == "Test Shop"
    assert "id" in shop
