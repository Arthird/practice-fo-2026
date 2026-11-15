from app.db.db import SessionLocal
from app.db import crud


def main() -> None:
    with SessionLocal() as session:
        categories = crud.get_categories(session)
        if not categories:
            print("БД пуста — запустите `python -m app.init_db`")
            return

        for cat in categories:
            print(f"\n=== {cat.title} ===")
            books = crud.get_books_by_category(session, cat.id)
            if not books:
                print("  (нет книг)")
                continue
            for b in books:
                print(f"• {b.title} — {b.price} ₽")
                print(f"  описание: {b.description}")
                print(f"  url:      {b.url or '—'}")


if __name__ == "__main__":
    main()