# Roadmap — Sync KPIs API

Este roadmap está pensado como **tutorial**: cada hito tiene objetivos de aprendizaje, entregables y criterios de aceptación (cómo saber que lo has hecho bien).

---
## M0 — Scaffold & Calidad
**Aprendes:** estructura FastAPI, configuración por entorno, linters, tests mínimos.
**Entrega:** app vacía con `/openapi.json`, pre‑commit, pytest, Docker Compose con MySQL, SQLite para dev.
**Aceptación:** `pytest` pasa; `pre-commit run --all-files` sin errores; `GET /openapi.json` → 200.

---
## M1 — Auth & Tenancy
**Aprendes:** JWT con python‑jose, hashing con passlib, dependencias de FastAPI; multi‑tenant básico.
**Entrega:** `User`, `Shop`; `POST /auth/register`, `POST /auth/login`, `POST /shops` (protegido).
**Aceptación:** puedes registrar, loguear y crear una shop; sin token → 401.

---
## M2 — Catálogo & Órdenes con Idempotencia
**Aprendes:** modelos relacionales, transacciones, claves únicas, cabeceras personalizadas.
**Entrega:** `Product`, `Receipt`, `ReceiptLine`, `IdemKey`; `POST /products`; `POST /shops/{id}/receipts` con `Idempotency-Key`.
**Aceptación:** repetir la misma `Idempotency-Key` devuelve el mismo `receipt_id`; el total cuadra.

---
## M3 — KPIs
**Aprendes:** agregaciones SQL eficientes, selección/joins, límites y ordenaciones.
**Entrega:** `GET /shops/{id}/kpis?from&to` — tickets, revenue, top_skus.
**Aceptación:** con datos de ejemplo devuelve contadores correctos y top SKUs esperado.

---
## M4 — Pulido & Docs
**Aprendes:** documentación clara, DX, automatización CI.
**Entrega:** README final, ejemplos `curl/httpie`, tagging de routers, GitHub Actions (lint+tests).
**Aceptación:** pipeline verde en PR; README con instrucciones reproducibles.

---
## M5 — Extensiones (opcionales)
- Sync incremental (`/devices/sync`) con `since` + `updated_at` (LWW simple).
- Export de KPIs a CSV/JSON.
- Migraciones **Alembic** + índices útiles.
- Mini‑admin (por ejemplo, panel ligero con FastAPI Admin) o portar el dominio a **Django admin**.
- Rate limiting e idempotencia por tabla.