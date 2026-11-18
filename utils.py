def print_menu(dishes):
    print("\nМЕНЮ")
    for dish in dishes:
        print(f"{dish['id']}. {dish['name']} — {dish['price']} руб.")

def calculate_total(items, dishes):
    by_id = {dish["id"]: dish for dish in dishes}
    total = 0
    for item in items:
        dish = by_id.get(item["dish_id"])
        if dish:
            total += dish["price"] * item["quantity"]
    return total

def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Введите положительное целое число.")
