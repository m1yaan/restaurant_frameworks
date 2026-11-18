class Table:
    def __init__(self, number, capacity, table_id=None):
        self.id = table_id
        self.number = int(number)
        self.capacity = int(capacity)
        self.is_available = True

    def __str__(self):
        return f"Стол №{self.number}, мест: {self.capacity}"

    def can_seat(self, guests):
        return self.capacity >= int(guests)

    def to_dict(self):
        return {"id": self.id, "number": self.number, "capacity": self.capacity, "is_available": self.is_available}
