"""Pydantic-схемы: описывают, что API принимает и что возвращает.

В Pydantic v2 аналог старого ``orm_mode`` — это
``model_config = ConfigDict(from_attributes=True)``. Он позволяет схемам
читать данные прямо из объектов SQLAlchemy (Category/Book).
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ─────────────── Category ───────────────
class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class CategoryCreate(CategoryBase):
    """Тело запроса на создание категории."""


class CategoryUpdate(CategoryBase):
    """Тело запроса на обновление категории (нужно новое название)."""


class CategoryRead(CategoryBase):
    """Ответ клиенту: категория + её id."""

    id: int

    model_config = ConfigDict(from_attributes=True)


# ─────────────── Book ───────────────
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    url: Optional[str] = ""
    category_id: int


class BookCreate(BookBase):
    """Тело запроса на создание книги."""


class BookUpdate(BaseModel):
    """Обновление книги: все поля опциональны (PATCH-семантика)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookRead(BookBase):
    """Ответ клиенту: книга + её id."""

    id: int

    model_config = ConfigDict(from_attributes=True)
