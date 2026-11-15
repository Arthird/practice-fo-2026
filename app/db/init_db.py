from app.db.db import Base, engine, SessionLocal
from app.db import models  # noqa: F401 — регистрация таблиц в metadata
from app.db import crud


CATEGORIES = ["Фантастика", "Программирование"]

BOOKS = {
    "Фантастика": [
        ("Дюна", "Планета Арракис, специи и большая политика.", 890.0),
        ("451° по Фаренгейту", "Антиутопия о сожжении книг.", 540.0),
        ("Солярис", "Разумный океан и пределы познания.", 610.0),
    ],
    "Программирование": [
        ("Fluent Python", "Идиоматичный Python от Лучано Ромбу.", 1990.0),
        ("Designing Data-Intensive Applications",
         "Клеппман о распределённых системах.", 2450.0),
        ("Clean Code", "Практики чистого кода.", 1700.0),
    ],
}


def main() -> None:
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        categories: list[models.Category] = []
        for title in CATEGORIES:
            cat = crud.get_category_by_title(session, title)
            if cat is None:
                cat = crud.create_category(session, title)
            categories.append(cat)

        for cat in categories:
            for title, description, price in BOOKS[cat.title]:
                if crud.get_books_by_category(session, cat.id) and any(
                    b.title == title for b in crud.get_books_by_category(session, cat.id)
                ):
                    continue
                crud.create_book(
                    session,
                    title=title,
                    description=description,
                    price=price,
                    category_id=cat.id,
                    url="",
                )

    print("init_db: категории и книги добавлены")


if __name__ == "__main__":
    main()