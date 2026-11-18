from django.shortcuts import render
from db.database import get_connection
def home(request):
    with get_connection() as conn:
        counts = {
            "clients": conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0],
            "dishes": conn.execute("SELECT COUNT(*) FROM dishes").fetchone()[0],
            "orders": conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
        }
    return render(request, "core/home.html", {"counts": counts})
def dishes(request):
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, category, price FROM dishes ORDER BY name").fetchall()
    return render(request, "core/dishes.html", {"dishes": rows})
