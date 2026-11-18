import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename, default=None):
    path = DATA_DIR / filename
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return [] if default is None else default
    except json.JSONDecodeError as exc:
        raise ValueError(f"Файл {filename} содержит некорректный JSON") from exc

def save_json(filename, data):
    path = DATA_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
