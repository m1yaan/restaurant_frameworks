from datetime import datetime

class Order:
    def __init__(self, client, table, items=None, status="Новый", order_id=None):
        self.id = order_id
        self.client = client
        self.table = table
        self.items = items or []
        self.status = status
        self.created_at = datetime.now().isoformat(timespec="seconds")

    def add_dish(self, dish, quantity=1):
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self.items.append({"dish": dish, "quantity": quantity})

    def total(self):
        return sum(row["dish"].price * row["quantity"] for row in self.items)

    def __str__(self):
        return f"Заказ #{self.id or 'новый'}: {self.client.name}, стол {self.table.number}, {self.total():.2f} руб."

    def to_dict(self):
        return {
            "id": self.id, "client": self.client.to_dict(), "table": self.table.to_dict(),
            "items": [{"dish": row["dish"].to_dict(), "quantity": row["quantity"]} for row in self.items],
            "status": self.status, "created_at": self.created_at, "total": self.total()
        }
