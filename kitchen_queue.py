from config import DELAY_BUFFER
from data import order_items
from utils import minutes_since, get_int


def is_delayed(entry):
    return entry["status"] != "Ready" and minutes_since(entry["time"]) > entry["prep_time"] + DELAY_BUFFER


def view_queue():
    print("\n========== KITCHEN QUEUE ==========")
    if len(order_items) == 0:
        print("No orders in the queue.")
        return
    queue = sorted(order_items, key=lambda e: e["time"])   
    print(f"{'ID':<5}{'Time':<10}{'Table':<7}{'Item':<20}{'Qty':<5}{'Waiting':<10}{'Status':<11}")
    for e in queue:
        flag = "  !! DELAYED" if is_delayed(e) else ""
        print(f"{e['id']:<5}{e['time'].strftime('%H:%M:%S'):<10}{e['table']:<7}"
              f"{e['name']:<20}{e['qty']:<5}{str(minutes_since(e['time'])) + ' min':<10}"
              f"{e['status']:<11}{flag}")


def show_waiting_tables():
    print("\n========== WAITING TABLES ==========")
    waiting = {}
    for e in order_items:
        if e["status"] != "Ready":
            waiting[e["table"]] = waiting.get(e["table"], 0) + 1
    if not waiting:
        print("No tables are waiting. All items are ready!")
        return
    for table in sorted(waiting):
        print(f"Table {table}: {waiting[table]} item(s) still not ready")


def update_status():
    open_items = [e for e in order_items if e["status"] != "Ready"]
    if not open_items:
        print("\nNo pending items to update.")
        return
    view_queue()
    ids = [e["id"] for e in open_items]
    item_id = get_int("\nEnter item ID to update (0 to cancel): ", minimum=0)
    if item_id == 0:
        return
    if item_id not in ids:
        print("\nInvalid ID, or that item is already ready.")
        return
    entry = next(e for e in order_items if e["id"] == item_id)

    print("1. Preparing")
    print("2. Ready")
    status_choice = get_int("Select new status: ", minimum=1, maximum=2)
    entry["status"] = "Preparing" if status_choice == 1 else "Ready"
    print(f"\n{entry['name']} for Table {entry['table']} is now {entry['status']}.")


def status_menu():
    while True:
        print("\n========== UPDATE ITEM STATUS ==========")
        print("1. Update an item's status")
        print("2. Show waiting tables")
        print("3. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            update_status()
        elif choice == "2":
            show_waiting_tables()
        elif choice == "3":
            break
        else:
            print("\nInvalid choice!")
