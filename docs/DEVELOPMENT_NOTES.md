# TaskList — Tutorial paso a paso

> Sigue este checklist en orden. Marca cada casilla al completar.

## M0 — Scaffold & Calidad
- [ x ] Inicializa repo y entorno
  - [ x ] Crea `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`.
  - [ x ] Instala dependencias (fastapi, uvicorn, sqlalchemy, pydantic, jose, passlib, pymysql, pytest, ruff, black, pre-commit).
  - [ x ] Añade `pre-commit-config.yaml` y ejecuta `pre-commit install`.
- [ x ] Crea estructura `app/` con `main.py` minimal y `/health`.
- [ x ] Añade `tests/test_smoke.py` y verifica:
  ```bash
  pytest -q
  ```
- [ ] Arranca con Docker y abre docs:
  ```bash
  docker compose up -d --build
  open http://localhost:8000/docs
  ```
- [ x ] Commit: `chore(scaffold): fastapi skeleton + docker + pre-commit`

## M1 — Auth & Tenancy
- [ x ] Modelos `User`, `Shop` en `models.py`.
- [ x ] Utilidades de seguridad (`hash_password`, `verify_password`, `create_token`).
- [ x ] Endpoints `POST /auth/register` y `POST /auth/login`.
- [ x ] Dependencia `get_current_user` con `OAuth2PasswordBearer`.
- [ x ] Endpoint `POST /shops` (crea workspace). Proteger con JWT.
- [ x ] Probar con curl:
  ```bash
  # register
  curl -sX POST :8000/auth/register -H 'content-type: application/json' \
    -d '{"email":"demo@example.com","password":"ChangeMe123"}'
  # login → export TOKEN
  # create shop
  curl -sX POST :8000/shops -H "authorization: Bearer $TOKEN" -d '{"name":"Demo"}' -H 'content-type: application/json'
  ```
- [ x ] Commit: `feat(auth): jwt login/register + shops`

## M2 — Catálogo & Órdenes con Idempotencia
- [ x ] Modelos `Product`, `Receipt`, `ReceiptLine`, `IdemKey` con constraints.
- [ x ] `POST /products`.
- [ x ] `POST /shops/{shop_id}/receipts` con cálculo de total y guardado de líneas.
- [ x ] Idempotencia: si `Idempotency-Key` existe, devolver recibo previo.
- [ x ] Prueba rápida:
  ```bash
  curl -sX POST :8000/products -H "authorization: Bearer $TOKEN" \
    -H 'content-type: application/json' -d '{"sku":"COCA-500","name":"Coca 500","price":1.2}'

  curl -sX POST :8000/shops/1/receipts \
    -H "authorization: Bearer $TOKEN" -H 'content-type: application/json' \
    -H 'Idempotency-Key: abc123' \
    -d '{"lines":[{"sku":"COCA-500","qty":2,"unit_price":1.2}]}'

  # Repite el mismo request y confirma el mismo receipt_id
  ```
- [ x ] Commit: `feat(orders): receipts with idempotency`

## M3 — KPIs
- [ x ] Consulta agregada: nº tickets, suma de total, top SKUs (join product/lines/receipts).
- [ x ] `GET /shops/{shop_id}/kpis?from&to` (filtrado por `created_at` si está disponible).
- [ x ] Prueba:
  ```bash
  curl -s :8000/shops/1/kpis
  ```
- [ x ] Commit: `feat(kpis): basic metrics endpoints`

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