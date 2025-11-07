from fastapi import FastAPI

app = FastAPI(title="Sync KPIs API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
