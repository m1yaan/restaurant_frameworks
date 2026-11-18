class Dish:
    def __init__(self, name, price, category="Основное", dish_id=None):
        self.id = dish_id
        self.name = name
        self.price = float(price)
        self.category = category

    def __str__(self):
        return f"{self.name} — {self.price:.2f} руб."

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}
