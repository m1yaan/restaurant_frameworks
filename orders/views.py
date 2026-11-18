from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, F, Q
from .models import Client, Table, Dish, Order

def dashboard(request):
    all_dishes = Dish.objects.all()                                      # 1
    available_dishes = Dish.objects.filter(is_available=True)           # 2
    hot_dishes = Dish.objects.filter(category__icontains="горяч")        # 3
    dishes_by_price = Dish.objects.order_by("price")                    # 4
    clients = Client.objects.order_by("name")                            # 5
    searched_clients = Client.objects.filter(Q(name__icontains="анна") | Q(phone__icontains="999")) # 6
    large_tables = Table.objects.filter(capacity__gte=4, is_active=True) # 7
    orders = Order.objects.select_related("client", "table").all()       # 8
    new_orders = Order.objects.filter(status="new")                      # 9
    recent_orders = Order.objects.order_by("-created_at")[:5]            # 10
    client_order_counts = Client.objects.annotate(order_count=Count("orders")) # 11
    average_price = Dish.objects.aggregate(value=Avg("price"))["value"]  # 12
    dish_sales = Dish.objects.annotate(sold=Sum("orderitem__quantity")).order_by("-sold") # 13
    order_totals = Order.objects.annotate(total=Sum(F("orderitem__quantity") * F("orderitem__dish__price"))) # 14
    page = Paginator(orders, 5).get_page(request.GET.get("page"))        # 15: pagination
    context = {"dishes": dishes_by_price, "clients": clients, "orders": page,
               "available_count": available_dishes.count(), "hot_count": hot_dishes.count(),
               "searched_count": searched_clients.count(), "large_tables": large_tables,
               "new_count": new_orders.count(), "recent_orders": recent_orders,
               "client_order_counts": client_order_counts, "average_price": average_price,
               "dish_sales": dish_sales, "order_totals": order_totals, "all_count": all_dishes.count()}
    return render(request, "orders/dashboard.html", context)
