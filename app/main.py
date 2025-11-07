from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routers import auth_router, shops_router
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (de momento nada)


app = FastAPI(title="Sync KPIs API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router.router)
app.include_router(shops_router.router)
