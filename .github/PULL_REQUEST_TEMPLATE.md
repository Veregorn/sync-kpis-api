# Título del PR

## Resumen
Breve descripción del cambio y el problema que resuelve.

## Tipo de cambio
- [ ] Feature
- [ ] Fix
- [ ] Docs
- [ ] Chore/CI

## Contexto / Issue
Referencia a ticket o milestone (si aplica).

## Checklist de calidad
- [ ] Código tipado y limpio (sin `ruff` warnings relevantes)
- [ ] `black --check` pasa
- [ ] Tests añadidos/actualizados y `pytest -q` pasa
- [ ] Endpoints documentados (descripción, summary/tags en OpenAPI)
- [ ] README/ROADMAP actualizados si procede

## Cómo probar (pasos)
Incluye comandos `curl`/`httpie`/Postman y datos de ejemplo.

```bash
# ejemplo rápido (ajusta TOKEN/shop_id según tu caso)
pytest -q
curl -s :8000/openapi.json | jq '.info'
```

## Criterios de aceptación
- [ ] Cumple los criterios del hito del **ROADMAP** correspondiente (M0/M1/M2/M3/M4/M5).

## Riesgos / Rollback
Riesgos conocidos, migraciones, cómo revertir si algo falla.

## Notas adicionales
Screenshots/logs si aporta valor.