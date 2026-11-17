from datetime import datetime
import data
from config import MAX_TABLE, MAX_QTY
from utils import get_int
from menu_manager import show_menu


def take_order():
    print("\n========== TAKE NEW ORDER ==========")
    if len(data.menu) == 0:
        print("Menu is empty. Add food items first.")
        return

    table = get_int(f"Enter table number (1-{MAX_TABLE}): ", minimum=1, maximum=MAX_TABLE)
    added = 0

    while True:
        show_menu()
        number = get_int("\nEnter item number (0 to finish): ", minimum=0, maximum=len(data.menu))
        if number == 0:
            break
        item = data.menu[number - 1]
        qty = get_int(f"Quantity of {item['name']} (1-{MAX_QTY}): ", minimum=1, maximum=MAX_QTY)

        data.order_items.append({
            "id": data.next_order_id,
            "table": table,
            "name": item["name"],
            "qty": qty,
            "price": item["price"],
            "prep_time": item["prep_time"],
            "status": "Pending",
            "time": datetime.now(),
        })
        data.sales[item["name"]] = data.sales.get(item["name"], 0) + qty
        print(f"Added {qty} x {item['name']} (Order #{data.next_order_id}).")
        data.next_order_id += 1
        added += 1

    if added == 0:
        print("\nNo items ordered.")
    else:
        print(f"\nOrder for Table {table} sent to the kitchen!")
