from django.shortcuts import render
from db.database import get_connection
def order_list(request):
    sql = """SELECT o.id, c.name, t.number, o.status, COALESCE(SUM(oi.quantity*d.price),0) AS total
             FROM orders o JOIN clients c ON c.id=o.client_id JOIN restaurant_tables t ON t.id=o.table_id
             LEFT JOIN order_items oi ON oi.order_id=o.id LEFT JOIN dishes d ON d.id=oi.dish_id
             GROUP BY o.id, c.name, t.number, o.status ORDER BY o.id DESC"""
    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()
    return render(request, "orders/list.html", {"orders": rows})
