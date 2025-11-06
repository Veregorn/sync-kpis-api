# Sync KPIs API (FastAPI + SQL)

Backend genérico para apps que generan **órdenes** (ventas/pedidos/reservas) y necesitan **autenticación**, **almacenamiento SQL** e **indicadores de negocio (KPIs)**. Útil como plantilla de backend serio para side‑projects, PoCs o pequeños productos (kioskos, e‑commerce ligero, clubs, ferias, food‑trucks, etc.).

## Características (MVP)
- Auth **JWT** (registro / login).
- Modelo multi‑tenant con **workspaces/shops**.
- **Catálogo** de items/productos.
- **Órdenes** con líneas + **idempotencia** (cabecera `Idempotency-Key`).
- **KPIs** por workspace: Nº de órdenes, revenue, top SKUs.
- **OpenAPI** docs, **tests**, **pre‑commit** (Black+Ruff), **Docker Compose** con MySQL. (Soporta SQLite para desarrollo rápido).

## Stack
- **Python 3.12**, **FastAPI**, **SQLAlchemy 2.x**, **Pydantic v2**.
- **MySQL 8** (o **SQLite** en local), **uvicorn**.
- Calidad: **pytest**, **ruff**, **black**, pre‑commit hooks.

## Estructura
```
app/
  main.py           # Enrutado principal
  deps.py           # Dependencias (DB, auth)
  database.py       # Engine + session + Base
  models.py         # SQLAlchemy models
  schemas.py        # Pydantic schemas
  crud.py           # Capa de acceso/consultas
  routers/          # Routers por dominio
    auth_router.py
    shops_router.py
    products_router.py
    receipts_router.py
    kpis_router.py
tests/
  test_smoke.py
Dockerfile
docker-compose.yml
pyproject.toml
pre-commit-config.yaml
.env.example
```

## Puesta en marcha
### Opción 1: Docker (recomendada)
```bash
docker compose up -d --build
# Docs
open http://localhost:8000/docs
```

### Opción 2: Local (SQLite)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # o usa pyproject con pipx/pip
export DB_URL=sqlite:///./dev.db
uvicorn app.main:app --reload
```

## API (MVP)
- `POST /auth/register` → Token.
- `POST /auth/login` → Token.
- `POST /shops` → Crea workspace/tienda.
- `POST /products` → Alta de producto.
- `POST /shops/{shop_id}/receipts` → Crea orden con líneas (**Idempotency-Key** opcional).
- `GET  /shops/{shop_id}/kpis?from=YYYY-MM-DD&to=YYYY-MM-DD` → Métricas básicas.

## Calidad y tests
```bash
pre-commit install
pytest -q
```

## Licencia
MIT