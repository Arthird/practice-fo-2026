"""Роуты для категорий: /categories (CRUD)."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    """Список всех категорий."""
    return crud.get_categories(db)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Категория по id."""
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория id={category_id} не найдена",
        )
    return category


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """Создать категорию. 201 Created при успехе."""
    if crud.get_category_by_title(db, payload.title) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Категория '{payload.title}' уже существует",
        )
    return crud.create_category(db, title=payload.title)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)
):
    """Обновить категорию."""
    existing = crud.get_category_by_title(db, payload.title)
    if existing is not None and existing.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Категория '{payload.title}' уже существует",
        )
    category = crud.update_category(db, category_id, title=payload.title)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория id={category_id} не найдена",
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию (каскадно удаляются её книги)."""
    if not crud.delete_category(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория id={category_id} не найдена",
        )
