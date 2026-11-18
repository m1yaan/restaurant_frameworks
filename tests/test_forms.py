from datetime import timedelta

import pytest
from django.test import Client as HttpClient
from django.utils import timezone

from orders.forms import OrderForm
from orders.models import Client, Order, Table


def _stamp(moment):
    return timezone.localtime(moment).strftime("%Y-%m-%dT%H:%M")


@pytest.mark.django_db
def test_order_form_rejects_past_reservation():
    client = Client.objects.create(name="Анна", phone="+79991110001")
    table = Table.objects.create(number=11, capacity=4)
    form = OrderForm(data={
        "client": client.pk,
        "table": table.pk,
        "status": "new",
        "guests": 2,
        "reservation_at": _stamp(timezone.now() - timedelta(days=1)),
    })

    assert form.is_valid() is False
    assert "reservation_at" in form.errors


@pytest.mark.django_db
def test_order_form_rejects_table_without_enough_seats():
    client = Client.objects.create(name="Пётр", phone="+79991110002")
    table = Table.objects.create(number=12, capacity=2)
    form = OrderForm(data={
        "client": client.pk,
        "table": table.pk,
        "status": "new",
        "guests": 5,
        "reservation_at": _stamp(timezone.now() + timedelta(days=1)),
    })

    assert form.is_valid() is False
    assert "table" in form.errors


@pytest.mark.django_db
def test_order_is_created_by_post():
    client = Client.objects.create(name="Мария", phone="+79991110003")
    table = Table.objects.create(number=13, capacity=4)
    response = HttpClient().post("/orders/add/", data={
        "client": client.pk,
        "table": table.pk,
        "status": "new",
        "guests": 2,
        "reservation_at": _stamp(timezone.now() + timedelta(days=1)),
    })

    assert response.status_code == 302
    assert Order.objects.filter(client=client, table=table, status="new").exists()
