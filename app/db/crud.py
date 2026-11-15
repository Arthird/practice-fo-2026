from typing import List, Optional, TypedDict, Unpack
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Category, Book


# ─────────────── Category ───────────────
def create_category(session: Session, title: str) -> Category:
    cat = Category(title=title)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


def get_category(session: Session, category_id: int) -> Optional[Category]:
    return session.get(Category, category_id)


def get_category_by_title(session: Session, title: str) -> Optional[Category]:
    return session.scalars(select(Category).where(Category.title == title)).first()


def get_categories(session: Session) -> List[Category]:
    return list(session.scalars(select(Category).order_by(Category.id)))


def update_category(session: Session, category_id: int, title: str) -> Optional[Category]:
    cat = session.get(Category, category_id)
    if cat is None:
        return None
    cat.title = title
    session.commit()
    session.refresh(cat)
    return cat


def delete_category(session: Session, category_id: int) -> bool:
    cat = session.get(Category, category_id)
    if cat is None:
        return False
    session.delete(cat)          # cascade удалит все книги категории
    session.commit()
    return True


# ─────────────── Book ───────────────
def create_book(
    session: Session,
    title: str,
    description: str,
    price: float,
    category_id: int,
    url: str = "",
) -> Book:
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def get_book(session: Session, book_id: int) -> Optional[Book]:
    return session.get(Book, book_id)


def get_books(session: Session) -> List[Book]:
    return list(session.scalars(select(Book).order_by(Book.id)))


def get_books_by_category(session: Session, category_id: int) -> List[Book]:
    return list(
        session.scalars(select(Book).where(Book.category_id == category_id))
    )


class BookUpdate(TypedDict, total=False):
    title: str
    description: Optional[str]
    price: float
    category_id: int
    url: Optional[str]


def update_book(
    session: Session, book_id: int, **fields: Unpack[BookUpdate]
) -> Optional[Book]:
    book = session.get(Book, book_id)
    if book is None:
        return None
    for key, value in fields.items():
        setattr(book, key, value)
    session.commit()
    session.refresh(book)
    return book


def delete_book(session: Session, book_id: int) -> bool:
    book = session.get(Book, book_id)
    if book is None:
        return False
    session.delete(book)
    session.commit()
    return True
