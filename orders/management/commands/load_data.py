"""Загрузка clients.json, dishes.json и orders.json в модели Django."""

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from orders.models import Client, Dish, Order, OrderItem, Table

STATUS_MAP = {
    "new": "new",
    "новый": "new",
    "cooking": "cooking",
    "готовится": "cooking",
    "ready": "ready",
    "готов": "ready",
    "paid": "paid",
    "оплачен": "paid",
    "cancelled": "cancelled",
    "отменён": "cancelled",
    "отменен": "cancelled",
}


class Command(BaseCommand):
    help = (
        "Читает JSON-справочники и заказы и создаёт Client, Dish, "
        "Table и Order через ORM. Повторный запуск обновляет те же записи."
    )

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR)
        client_rows = self._read_catalogs(
            [base / "data" / "clients.json", base / "db" / "clients.json"]
        )
        dish_rows = self._read_catalogs(
            [base / "data" / "dishes.json", base / "db" / "dishes.json"]
        )
        orders = []
        for path in (
            base / "orders.json",
            base / "data" / "orders.json",
            base / "db" / "orders.json",
        ):
            orders.extend(self._read_list(path))

        if not client_rows and not dish_rows and not orders:
            raise CommandError(
                "Не найдены clients.json, dishes.json или orders.json."
            )

        with transaction.atomic():
            for row in client_rows:
                self._save_client(row)
            for row in dish_rows:
                self._save_dish(row)
            for row in orders:
                self._save_order(row)

        self.stdout.write(self.style.SUCCESS(
            "Импорт завершён. В базе: "
            f"клиентов {Client.objects.count()}, "
            f"блюд {Dish.objects.count()}, "
            f"столов {Table.objects.count()}, "
            f"заказов {Order.objects.count()}, "
            f"позиций {OrderItem.objects.count()}."
        ))

    def _read_catalogs(self, paths):
        rows = []
        for path in paths:
            rows.extend(self._read_list(path))
        return rows

    def _read_list(self, path):
        if not path.exists():
            return []
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(
                f"{path.name}: некорректный JSON ({exc})"
            ) from exc
        if isinstance(payload, dict):
            return [payload]
        if not isinstance(payload, list):
            raise CommandError(f"{path.name}: ожидался список объектов JSON.")
        self.stdout.write(f"Прочитан {path.relative_to(settings.BASE_DIR)}")
        return [row for row in payload if isinstance(row, dict)]

    def _save_client(self, row):
        phone = str(row.get("phone") or "").strip()
        name = str(row.get("name") or "").strip()
        if not phone or not name:
            self.stderr.write("Пропущен клиент без имени или телефона.")
            return False
        email = str(row.get("email") or "").strip()
        client, created = Client.objects.get_or_create(
            phone=phone[:20],
            defaults={"name": name[:120], "email": email},
        )
        if created:
            return True
        changed = []
        if client.name != name[:120]:
            client.name = name[:120]
            changed.append("name")
        if email and client.email != email:
            client.email = email
            changed.append("email")
        if changed:
            client.save(update_fields=changed)
        return True

    def _save_dish(self, row):
        name = str(row.get("name") or "").strip()
        category = str(row.get("category") or "Основное").strip() or "Основное"
        if not name:
            self.stderr.write("Пропущено блюдо без названия.")
            return False
        try:
            price = Decimal(str(row.get("price", "0")))
        except (InvalidOperation, ValueError):
            self.stderr.write(f"Пропущено блюдо «{name}»: некорректная цена.")
            return False
        if price < 0:
            self.stderr.write(f"Пропущено блюдо «{name}»: отрицательная цена.")
            return False
        defaults = {"category": category[:80], "price": price}
        dish, created = Dish.objects.get_or_create(
            name=name[:120],
            defaults=defaults,
        )
        if not created:
            dish.category = defaults["category"]
            dish.price = price
            dish.save(update_fields=["category", "price"])
        return True

    def _save_table(self, row):
        if not isinstance(row, dict):
            return None
        number = row.get("number")
        capacity = row.get("capacity")
        if number is None or capacity is None:
            return None
        try:
            number = int(number)
            capacity = int(capacity)
        except (TypeError, ValueError):
            return None
        if number < 1 or capacity < 1:
            return None
        is_active = row.get("is_active", row.get("is_available", True))
        table, _created = Table.objects.get_or_create(
            number=number,
            defaults={"capacity": capacity, "is_active": bool(is_active)},
        )
        table.capacity = capacity
        table.is_active = bool(is_active)
        table.save(update_fields=["capacity", "is_active"])
        return table

    def _save_order(self, row):
        raw_client = row.get("client")
        client_row = raw_client if isinstance(raw_client, dict) else None
        if client_row:
            self._save_client(client_row)
        phone = ""
        if client_row:
            phone = str(client_row.get("phone") or "").strip()[:20]
        client = Client.objects.filter(phone=phone).first() if phone else None
        if client is None:
            self.stderr.write("Пропущен заказ: клиент не найден.")
            return

        table = self._save_table(row.get("table"))
        if table is None:
            self.stderr.write(
                f"Пропущен заказ клиента {client}: в JSON нет стола."
            )
            return

        status = self._status(row.get("status"))
        created_at = self._aware(row.get("created_at"))
        order = Order.objects.filter(
            client=client,
            table=table,
            created_at=created_at,
        ).first()
        if order is None:
            order = Order.objects.create(
                client=client,
                table=table,
                status=status,
                reservation_at=created_at,
            )
            Order.objects.filter(pk=order.pk).update(created_at=created_at)
        elif order.status != status:
            order.status = status
            order.save(update_fields=["status"])

        OrderItem.objects.filter(order=order).delete()
        for item in row.get("items") or []:
            if not isinstance(item, dict):
                continue
            raw_dish = item.get("dish")
            dish_row = raw_dish if isinstance(raw_dish, dict) else item
            if not self._save_dish(dish_row):
                continue
            dish_name = str(dish_row.get("name") or "").strip()[:120]
            dish = Dish.objects.filter(name=dish_name).first()
            try:
                quantity = int(item.get("quantity") or 1)
            except (TypeError, ValueError):
                quantity = 0
            if dish is None or quantity < 1:
                continue
            OrderItem.objects.create(order=order, dish=dish, quantity=quantity)

    def _status(self, raw):
        key = str(raw or "new").strip().lower()
        return STATUS_MAP.get(key, "new")

    def _aware(self, raw):
        parsed = parse_datetime(str(raw)) if raw else None
        if parsed is None:
            parsed = timezone.now()
        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(
                parsed, timezone.get_current_timezone()
            )
        return parsed
