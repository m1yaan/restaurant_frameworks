from django.shortcuts import render
ORDERS = [
    {"id": 1, "client": "Анна Иванова", "table": 2, "status": "Новый", "total": 870},
    {"id": 2, "client": "Иван Петров", "table": 4, "status": "Готов", "total": 520},
]
def order_list(request):
    return render(request, "orders/list.html", {"orders": ORDERS})
