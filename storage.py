import json
from pathlib import Path

class JsonStorage:
    def __init__(self, filename="orders.json"):
        self.path = Path(__file__).parent / filename

    def save(self, objects):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump([obj.to_dict() for obj in objects], file, ensure_ascii=False, indent=2)

    def load_raw(self):
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as file:
            return json.load(file)
