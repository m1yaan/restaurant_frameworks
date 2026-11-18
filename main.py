from storage import load_json
from utils import print_menu, calculate_total, read_positive_int

def main():
    clients = load_json("clients.json")
    dishes = load_json("dishes.json")
    print("Клиенты:")
    for client in clients:
        print(f"{client['id']}. {client['name']} ({client['phone']})")
    name = input("Имя клиента для заказа: ").strip() or "Гость"
    print_menu(dishes)
    items = []
    while True:
        raw = input("ID блюда (Enter — закончить): ").strip()
        if not raw:
            break
        try:
            dish_id = int(raw)
        except ValueError:
            print("ID должен быть числом.")
            continue
        if not any(d["id"] == dish_id for d in dishes):
            print("Блюдо не найдено.")
            continue
        items.append({"dish_id": dish_id, "quantity": read_positive_int("Количество: ")})
    print(f"Клиент: {name}")
    print(f"Итого: {calculate_total(items, dishes)} руб.")

if __name__ == "__main__":
    main()
