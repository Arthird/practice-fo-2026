Практика 2026 в [Форусе](https://forus.ru)

## Запуск

```bash
docker compose up --build
```

Поднимаются два сервиса: PostgreSQL (`db`, порт `5439`) и приложение (`app`, порт `8000`).
При старте создаются таблицы и выполняется наполнение БД (`app.db.init_db`), затем
запускается Uvicorn.

Проверка:

- Swagger: http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

## Запуск локально (без Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload
```

Требуются переменные окружения из `.env` (доступ к PostgreSQL).

## API

`GET /health` — статус сервиса.

Категории (`/categories`):

- `GET /categories/` — список категорий
- `GET /categories/{category_id}` — категория по id
- `POST /categories/` — создать (201, 409 если название занято)
- `PUT /categories/{category_id}` — обновить
- `DELETE /categories/{category_id}` — удалить (204, каскадно удаляет книги)

Книги (`/books`):

- `GET /books/?category_id=` — список книг, фильтр по категории
- `GET /books/{book_id}` — книга по id
- `POST /books/` — создать (201, 400 если категории нет)
- `PUT /books/{book_id}` — обновить (частично)
- `DELETE /books/{book_id}` — удалить (204)

Пример:

```bash
curl -X POST http://127.0.0.1:8000/categories/ -H 'Content-Type: application/json' \
  -d '{"title": "Фантастика"}'

curl -X POST http://127.0.0.1:8000/books/ -H 'Content-Type: application/json' \
  -d '{"title": "Дюна", "description": "…", "price": 890, "category_id": 1}'
```

## Структура

- `app/main.py` — точка входа FastAPI, подключение роутеров, `/health`
- `app/schemas.py` — Pydantic-схемы (from_attributes)
- `app/api/books.py`, `app/api/categories.py` — роутеры CRUD
- `app/db/models.py` — ORM-модели `Category`, `Book`
- `app/db/crud.py` — функции доступа к данным
- `app/db/db.py` — engine, `SessionLocal`, зависимость `get_db`
- `app/db/init_db.py` — создание таблиц и наполнение БД
