"""Роуты для книг: /books (CRUD + фильтр по категории)."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


def _ensure_category_exists(db: Session, category_id: int) -> None:
    """Бизнес-валидация: книга обязана ссылаться на существующую категорию."""
    if crud.get_category(db, category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория id={category_id} не существует",
        )


@router.get("/", response_model=List[BookRead])
def list_books(
    category_id: Optional[int] = Query(None, description="Фильтр по id категории"),
    db: Session = Depends(get_db),
):
    """Список книг; можно отфильтровать по категории через ?category_id=."""
    if category_id is not None:
        return crud.get_books_by_category(db, category_id)
    return crud.get_books(db)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Книга по id."""
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга id={book_id} не найдена",
        )
    return book


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    """Создать книгу. 201 Created при успехе."""
    _ensure_category_exists(db, payload.category_id)
    return crud.create_book(
        db,
        title=payload.title,
        description=payload.description if payload.description else "",
        price=payload.price,
        category_id=payload.category_id,
        url=payload.url or "",
    )


@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу (передаются только изменяемые поля)."""
    if crud.get_book(db, book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга id={book_id} не найдена",
        )

    fields = payload.model_dump(exclude_unset=True)
    if fields.get("category_id") is not None:
        _ensure_category_exists(db, fields["category_id"])

    book = crud.update_book(db, book_id, **fields)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу."""
    if not crud.delete_book(db, book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга id={book_id} не найдена",
        )
