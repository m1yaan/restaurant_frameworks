from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Order, Dish
from .forms import ClientForm, OrderForm, DishPhotoForm


def dashboard(request):
    return render(request,
                  "orders/dashboard.html",
                  {"orders": Order.objects.select_related("client",
                                                          "table")[:20],
                   "dishes": Dish.objects.all()})


def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Клиент создан.")
        return redirect("dashboard")
    return render(request, "orders/form.html", {"form": form, "title": "Новый клиент"})


def client_edit(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Клиент обновлён.")
        return redirect("dashboard")
    return render(request, "orders/form.html", {"form": form, "title": "Редактирование клиента"})


def client_delete(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Клиент удалён.")
        return redirect("dashboard")
    return render(request, "orders/confirm_delete.html", {"object": obj})


def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Заказ создан.")
        return redirect("dashboard")
    return render(request, "orders/form.html", {"form": form, "title": "Новый заказ"})


def order_edit(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Заказ обновлён.")
        return redirect("dashboard")
    return render(request, "orders/form.html", {"form": form, "title": "Редактирование заказа"})


def order_delete(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Заказ удалён.")
        return redirect("dashboard")
    return render(request, "orders/confirm_delete.html", {"object": obj})


def dish_photo(request, pk):
    obj = get_object_or_404(Dish, pk=pk)
    form = DishPhotoForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Фото блюда сохранено.")
        return redirect("dashboard")
    return render(request, "orders/form.html", {"form": form, "title": f"Фото блюда: {obj.name}"})
