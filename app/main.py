from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routers import auth_router, shops_router, products_router, receipts_router
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (de momento nada)


app = FastAPI(title="Sync KPIs API", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth_router.router)
app.include_router(shops_router.router)
app.include_router(products_router.router)
app.include_router(receipts_router.router)
