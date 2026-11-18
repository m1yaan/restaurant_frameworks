# Сервис управления ресторанными заказами — ПР10 — административная панель

Настроены list_display, list_filter, search_fields и Inline для состава заказа. Подключён Django Debug Toolbar. Создайте администратора командой `python manage.py createsuperuser`; админка доступна по `/admin/`, toolbar — по `/__debug__/`.

## Запуск
Для консольных этапов: `python main.py`.

Для Django-этапов:
1. Создайте виртуальное окружение: `python -m venv .venv`
2. Активируйте его.
3. Установите зависимости: `pip install -r requirements.txt`
4. Выполните миграции (если предусмотрены): `python manage.py migrate`
5. Запустите сервер: `python manage.py runserver`

Язык интерфейса Django: русский (`ru-ru`).
