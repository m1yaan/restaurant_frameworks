from models import Client, Dish, Table, Order
from storage import JsonStorage

def main():
    client = Client(input("Имя клиента: ").strip() or "Гость", input("Телефон: ").strip() or "не указан", 1)
    table = Table(1, 4, 1)
    guests = int(input("Количество гостей: ") or "1")
    if not table.can_seat(guests):
        print("Вместимость стола недостаточна.")
        return
    menu = [
        Dish("Борщ", 350, "Первое", 1),
        Dish("Паста Карбонара", 520, "Горячее", 2),
        Dish("Чай", 120, "Напитки", 3),
    ]
    for dish in menu:
        print(f"{dish.id}. {dish}")
    order = Order(client, table)
    while True:
        raw = input("ID блюда (Enter — завершить): ").strip()
        if not raw:
            break
        dish = next((item for item in menu if item.id == int(raw)), None)
        if dish:
            order.add_dish(dish, int(input("Количество: ") or "1"))
    order.id = 1
    JsonStorage().save([order])
    print(order)
    print("Заказ сохранён в orders.json")

if __name__ == "__main__":
    main()
