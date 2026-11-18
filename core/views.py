from django.shortcuts import render
DISHES = [
    {"name": "Борщ", "price": 350, "category": "Первое", "available": True},
    {"name": "Паста Карбонара", "price": 520, "category": "Горячее", "available": True},
    {"name": "Цезарь", "price": 430, "category": "Салаты", "available": False},
]
def home(request):
    return render(request, "core/home.html")
def dishes(request):
    return render(request, "core/dishes.html", {"dishes": DISHES})
