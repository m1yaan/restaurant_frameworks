class Client:
    def __init__(self, name, phone, client_id=None):
        self.id = client_id
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "phone": self.phone}
