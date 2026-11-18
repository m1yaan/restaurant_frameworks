# Сервис управления ресторанными заказами

Веб-сервис для учёта клиентов, столов, меню и заказов ресторана. Справочники и заказы хранятся в SQLite и доступны через страницы сайта и панель администратора Django.

## Стек

Python, Django 5.2, SQLite, Bootstrap 5, pytest, flake8.

## Установка и запуск

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_data
python manage.py createsuperuser
python manage.py runserver
```

Сайт открывается по адресу http://127.0.0.1:8000/. Панель администратора: http://127.0.0.1:8000/admin/.

Команда `load_data` читает `data/clients.json`, `data/dishes.json`, `db/clients.json`, `db/dishes.json` и `orders.json` и создаёт записи через ORM. Повторный запуск обновляет те же объекты и не создаёт дубликаты.

## Структура

- `manage.py` — точка входа команд Django.
- `restaurant/` — настройки, корневые маршруты, WSGI и ASGI.
- `orders/` — модели, формы, представления, админка и команда `load_data`.
- `core/` — стартовая страница, которая перенаправляет на список заказов.
- `templates/` — общие шаблоны и страницы заказов.
- `static/` — стили.
- `data/` и `db/` — JSON-справочники для первоначальной загрузки.
- `tests/` — тесты pytest.

## Сущности

- `Client` — имя, телефон, email.
- `Table` — номер, вместимость, признак активности.
- `Dish` — название, категория, цена, фото.
- `Order` — клиент, стол, статус и время бронирования.
- `OrderItem` — блюдо и количество в составе заказа.

## Проверки

```powershell
pytest
flake8
```

`pytest` проверяет сохранение моделей, строковое представление, запрет брони в прошлом, вместимость стола и создание заказа через форму. `flake8` проверяет стиль по правилам из `.flake8`.
