import json

MENU = [
    {"id": 1, "name": "Борщ", "price": 350},
    {"id": 2, "name": "Паста Карбонара", "price": 520},
    {"id": 3, "name": "Цезарь", "price": 430},
    {"id": 4, "name": "Чай", "price": 120},
]

def show_menu():
    print("\nМЕНЮ")
    for dish in MENU:
        print(f"{dish['id']}. {dish['name']} — {dish['price']} руб.")

def main():
    print("=== Сервис управления ресторанными заказами ===")
    client_name = input("Введите имя клиента: ").strip() or "Гость"
    show_menu()
    total = 0
    selected = []
    while True:
        choice = input("\nВведите номер блюда (Enter — завершить): ").strip()
        if not choice:
            break
        if not choice.isdigit():
            print("Введите числовой номер блюда.")
            continue
        dish = next((item for item in MENU if item["id"] == int(choice)), None)
        if dish is None:
            print("Такого блюда нет в меню.")
            continue
        qty_text = input("Количество: ").strip()
        try:
            qty = int(qty_text)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Количество должно быть положительным целым числом.")
            continue
        subtotal = dish["price"] * qty
        total += subtotal
        selected.append({"dish": dish["name"], "quantity": qty, "subtotal": subtotal})
        print(f"Добавлено: {dish['name']} × {qty} = {subtotal} руб.")
    print("\n--- Чек ---")
    print(f"Клиент: {client_name}")
    for item in selected:
        print(f"{item['dish']} × {item['quantity']} — {item['subtotal']} руб.")
    print(f"Итого: {total} руб.")
    print("Спасибо за заказ!")

if __name__ == "__main__":
    main()
