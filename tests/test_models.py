from datetime import timedelta

import pytest
from django.utils import timezone

from orders.models import Client, Dish, Order, Table


@pytest.mark.django_db
def test_client_is_saved_and_str_returns_name():
    client = Client.objects.create(name="Анна Иванова", phone="+79990001122")

    assert client.pk is not None
    assert str(client) == "Анна Иванова"


@pytest.mark.django_db
def test_table_is_saved_and_str_returns_number():
    table = Table.objects.create(number=7, capacity=4)

    assert table.pk is not None
    assert str(table) == "Стол №7"


@pytest.mark.django_db
def test_dish_is_saved_and_str_returns_name():
    dish = Dish.objects.create(name="Борщ", category="Первое", price="350.00")

    assert dish.pk is not None
    assert str(dish) == "Борщ"


@pytest.mark.django_db
def test_order_is_saved_and_str_returns_number():
    client = Client.objects.create(name="Иван Петров", phone="+79990001123")
    table = Table.objects.create(number=8, capacity=2)
    order = Order.objects.create(
        client=client,
        table=table,
        reservation_at=timezone.now() + timedelta(days=1),
    )

    assert order.pk is not None
    assert str(order) == f"Заказ №{order.pk}"
