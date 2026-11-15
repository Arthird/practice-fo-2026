"""Точка входа FastAPI.

Запуск (из корня проекта):
    uvicorn app.main:app --reload

Документация (Swagger): http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import books, categories
from app.db.db import Base, engine
from app.db import models  # noqa: F401 — регистрация таблиц в metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    """На старте поднимаем таблицы (engine и SessionLocal уже настроены)."""
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Octagon Books API",
    description="Учебный API для категорий и книг (FastAPI + SQLAlchemy + PostgreSQL).",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(categories.router)
app.include_router(books.router)


@app.get("/health", tags=["service"])
def health() -> dict:
    """Проверка, что сервис жив."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
