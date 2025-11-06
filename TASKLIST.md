# TaskList — Tutorial paso a paso

> Sigue este checklist en orden. Marca cada casilla al completar.

## M0 — Scaffold & Calidad
- [ ] Inicializa repo y entorno
  - [ ] Crea `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`.
  - [ ] Instala dependencias (fastapi, uvicorn, sqlalchemy, pydantic, jose, passlib, pymysql, pytest, ruff, black, pre-commit).
  - [ ] Añade `pre-commit-config.yaml` y ejecuta `pre-commit install`.
- [ ] Crea estructura `app/` con `main.py` minimal y `/health`.
- [ ] Añade `tests/test_smoke.py` y verifica:
  ```bash
  pytest -q
  ```
- [ ] Arranca con Docker y abre docs:
  ```bash
  docker compose up -d --build
  open http://localhost:8000/docs
  ```
- [ ] Commit: `chore(scaffold): fastapi skeleton + docker + pre-commit`

## M1 — Auth & Tenancy
- [ ] Modelos `User`, `Shop` en `models.py`.
- [ ] Utilidades de seguridad (`hash_password`, `verify_password`, `create_token`).
- [ ] Endpoints `POST /auth/register` y `POST /auth/login`.
- [ ] Dependencia `get_current_user` con `OAuth2PasswordBearer`.
- [ ] Endpoint `POST /shops` (crea workspace). Proteger con JWT.
- [ ] Probar con curl:
  ```bash
  # register
  curl -sX POST :8000/auth/register -H 'content-type: application/json' \
    -d '{"email":"demo@example.com","password":"ChangeMe123"}'
  # login → export TOKEN
  # create shop
  curl -sX POST :8000/shops -H "authorization: Bearer $TOKEN" -d '{"name":"Demo"}' -H 'content-type: application/json'
  ```
- [ ] Commit: `feat(auth): jwt login/register + shops`

## M2 — Catálogo & Órdenes con Idempotencia
- [ ] Modelos `Product`, `Receipt`, `ReceiptLine`, `IdemKey` con constraints.
- [ ] `POST /products`.
- [ ] `POST /shops/{shop_id}/receipts` con cálculo de total y guardado de líneas.
- [ ] Idempotencia: si `Idempotency-Key` existe, devolver recibo previo.
- [ ] Prueba rápida:
  ```bash
  curl -sX POST :8000/products -H "authorization: Bearer $TOKEN" \
    -H 'content-type: application/json' -d '{"sku":"COCA-500","name":"Coca 500","price":1.2}'

  curl -sX POST :8000/shops/1/receipts \
    -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' \
    -H 'Idempotency-Key: abc123' \
    -d '{"lines":[{"sku":"COCA-500","qty":2,"unit_price":1.2}]}'

  # Repite el mismo request y confirma el mismo receipt_id
  ```
- [ ] Commit: `feat(orders): receipts with idempotency`

## M3 — KPIs
- [ ] Consulta agregada: nº tickets, suma de total, top SKUs (join product/lines/receipts).
- [ ] `GET /shops/{shop_id}/kpis?from&to` (filtrado por `created_at` si está disponible).
- [ ] Prueba:
  ```bash
  curl -s :8000/shops/1/kpis
  ```
- [ ] Commit: `feat(kpis): basic metrics endpoints`

## M4 — Pulido & Docs
- [ ] Etiquetas por router y descripciones en OpenAPI.
- [ ] README final (quickstart, API, estructura, tests, licencia).
- [ ] Añade GitHub Actions (lint + tests).
- [ ] Revisa `pre-commit run --all-files` y `pytest -q`.
- [ ] Commit: `docs(readme): usage & api`; `ci(actions): lint+tests`

## M5 — Extensiones (opcionales)
- [ ] Sync incremental (`/devices/sync`) con `since` y `updated_at`.
- [ ] Export KPIs CSV/JSON.
- [ ] Alembic + migraciones + índices.
- [ ] Rate limiting e idempotencia por tabla.
- [ ] Admin mínimo (FastAPI Admin o portar a Django admin).