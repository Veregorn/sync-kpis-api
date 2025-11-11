# Sync KPIs API

A small but production-oriented backend template built with **FastAPI** and **SQLAlchemy**.

The goal is to support applications that:

- manage **shops/workspaces**,
- store **orders/receipts** in a relational database,
- expose **business KPIs** (revenue, top SKUs, etc.),
- need **JWT authentication**, **multitenancy**, and **idempotent writes**.

It is intentionally generic: suitable for kiosks, small POS systems, light e-commerce, events, fairs, food trucks, etc.

---

## Features

**Authentication & Tenancy**

- User registration & login via **JWT**.
- `OAuth2PasswordBearer` for protected endpoints.
- Each user owns one or more **shops**.
- All write operations are scoped to the authenticated owner.

**Catalog & Orders**

- `Product` model with SKU, name, price.
- `Receipt` + `ReceiptLine` to persist sales.
- On-the-fly product creation from incoming lines (for simple integrations).

**Idempotent Receipt Creation**

- `POST /shops/{shop_id}/receipts` accepts `Idempotency-Key` header.
- Same key + same payload → returns the **same receipt**, does not duplicate.
- Useful for flaky networks, mobile clients, or retrying integrations.

**KPIs**

- `GET /shops/{shop_id}/kpis`:
  - total number of receipts,
  - total revenue,
  - top SKUs (quantity & revenue),
  - optional date range filter.

**Quality & Tooling**

- **FastAPI** + **Pydantic v2**.
- **SQLAlchemy 2.x** ORM style.
- `pytest` for integration-style tests:
  - smoke test,
  - auth flow (register → login → create shop),
  - idempotent receipts,
  - KPIs aggregation.
- **pre-commit** with:
  - `black`,
  - `ruff`,
  - `debug-statements` (no `pdb` / debug trash).
- **GitHub Actions**:
  - install from `pyproject.toml`,
  - lint + format check + tests on each push/PR.

---

## Tech Stack

- Python **3.11+**
- **FastAPI**
- **SQLAlchemy 2.x**
- **Pydantic v2** (`pydantic[email]`)
- **PyMySQL** (MySQL) or SQLite for local dev
- **python-jose**, **passlib[bcrypt]** for JWT & password hashing
- **Uvicorn** as ASGI server
- **pytest**, **ruff**, **black**, **pre-commit**

---

## Project Structure

app/
  main.py            # FastAPI app + router wiring
  database.py        # SQLAlchemy engine/session/Base
  models.py          # ORM models (User, Shop, Product, Receipt, ... )
  schemas.py         # Pydantic models (request/response)
  deps.py            # DB session & current_user dependencies
  utils/
    security.py      # Password hashing & JWT helpers
  routers/
    auth_router.py
    shops_router.py
    products_router.py
    receipts_router.py
    kpis_router.py
tests/
  test_smoke.py
  test_auth_flow.py
  test_receipts_idempotency.py
  test_kpis.py
.github/
  workflows/ci.yml   # lint + tests
pyproject.toml
Dockerfile
docker-compose.yml
.env.example

---

## Running Locally

1. Using SQLite (simple dev setup)

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env  # DB_URL=sqlite:///./dev.db

uvicorn app.main:app --reload

Open:
	•	API docs: http://localhost:8000/docs
	•	Health check: GET /health


2. Using Docker + MySQL

cp .env.example .env
# set DB_URL to:
# mysql+pymysql://sync_kpis_user:sync_kpis_pass@db:3306/sync_kpis_db

docker compose up -d --build

---

## Testing

pytest -q

CI runs the same suite on each push/PR.

---

## Notes

This project is intentionally small and focused.
	•	It aims to demonstrate:
	•	clean API design,
	•	proper auth & multitenancy,
	•	idempotent write patterns,
	•	SQL-based reporting / KPIs,
	•	modern Python tooling.

Feel free to fork and adapt it for real-world backends or technical screenings.