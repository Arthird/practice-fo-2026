import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""


def get_session():
    """Генератор сессии — удобно для `with`."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_db():
    """FastAPI-зависимость: одна сессия на запрос.

    Используется в эндпоинтах через ``Depends(get_db)`` — единый способ
    получить Session во всём API.
    """
    yield from get_session()
