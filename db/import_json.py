import json
from pathlib import Path
from database import get_connection, DB_PATH

DATA = Path(__file__).resolve().parent
def main():
    schema = (Path(__file__).resolve().parents[1] / "sql/schema.sql").read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(schema)
        clients = json.loads((DATA / "clients.json").read_text(encoding="utf-8"))
        dishes = json.loads((DATA / "dishes.json").read_text(encoding="utf-8"))
        conn.executemany("INSERT OR REPLACE INTO clients(id,name,phone) VALUES(?,?,?)",
                         [(x["id"],x["name"],x["phone"]) for x in clients])
        conn.executemany("INSERT OR REPLACE INTO dishes(id,name,category,price) VALUES(?,?,?,?)",
                         [(x["id"],x["name"],x["category"],x["price"]) for x in dishes])
        conn.execute("INSERT OR IGNORE INTO restaurant_tables(id,number,capacity) VALUES(1,1,4)")
        conn.execute("INSERT OR IGNORE INTO orders(id,client_id,table_id,status) VALUES(1,1,1,'Новый')")
        conn.execute("INSERT OR IGNORE INTO order_items(order_id,dish_id,quantity) VALUES(1,1,2)")
    print(f"Импорт завершён: {DB_PATH}")
if __name__ == "__main__":
    main()
