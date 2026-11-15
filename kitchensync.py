from datetime import datetime

TAX_RATE = 0.05          # 5% GST
DELAY_BUFFER = 10        # minutes added to prep time before an order is flagged (stretch)

# ---------------- DATA ----------------
menu = []                # {"name", "price", "prep_time"}
order_items = []         # one entry per ordered line, see take_order()
sales = {}               # item name -> total quantity sold today (stretch)
next_order_id = 1


# ---------------- INPUT HELPERS (handle wrong input) ----------------
def get_text(prompt):
    return input(prompt).strip()


def get_int(prompt, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and number < minimum:
            print(f"Value must be at least {minimum}.")
        elif maximum is not None and number > maximum:
            print(f"Value must be at most {maximum}.")
        else:
            return number


def get_float(prompt, minimum=0):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if number <= minimum:
            print(f"Value must be greater than {minimum}.")
        else:
            return number


def minutes_since(start):
    return int((datetime.now() - start).total_seconds() // 60)


def find_menu_item(name):
    for item in menu:
        if item["name"].lower() == name.lower():
            return item
    return None


# ---------------- FEATURE 1: MENU ----------------
def show_menu():
    print("\n========== FOOD MENU ==========")
    if len(menu) == 0:
        print("No food items available.")
        return
    print(f"{'No.':<5}{'Name':<22}{'Price':>10}{'Prep (min)':>13}")
    for i, item in enumerate(menu, start=1):
        print(f"{i:<5}{item['name']:<22}{item['price']:>10.2f}{item['prep_time']:>13}")


def manage_menu():
    while True:
        print("\n========== MANAGE MENU ==========")
        print("1. Add Food Item")
        print("2. View Menu")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            name = get_text("\nEnter food name: ")
            if name == "":
                print("\nFood name cannot be empty!")
            elif find_menu_item(name):
                print("\nThat item is already on the menu!")
            else:
                price = get_float("Enter price: ")
                prep_time = get_int("Enter preparation time (minutes): ", minimum=1)
                menu.append({"name": name, "price": price, "prep_time": prep_time})
                print("\nFood item added successfully!")

        elif choice == "2":
            show_menu()

        elif choice == "3":
            break

        else:
            print("\nInvalid choice!")


# ---------------- FEATURE 2: TAKE ORDER ----------------
def take_order():
    global next_order_id
    print("\n========== TAKE NEW ORDER ==========")
    if len(menu) == 0:
        print("Menu is empty. Add food items first.")
        return

    table = get_int("Enter table number: ", minimum=1)
    added = 0

    while True:
        show_menu()
        number = get_int("\nEnter item number (0 to finish): ", minimum=0, maximum=len(menu))
        if number == 0:
            break
        item = menu[number - 1]
        qty = get_int(f"Quantity of {item['name']}: ", minimum=1)

        order_items.append({
            "id": next_order_id,
            "table": table,
            "name": item["name"],
            "qty": qty,
            "price": item["price"],
            "prep_time": item["prep_time"],
            "status": "Pending",
            "time": datetime.now(),
        })
        sales[item["name"]] = sales.get(item["name"], 0) + qty
        print(f"Added {qty} x {item['name']} (Order #{next_order_id}).")
        next_order_id += 1
        added += 1

    if added == 0:
        print("\nNo items ordered.")
    else:
        print(f"\nOrder for Table {table} sent to the kitchen!")


# ---------------- FEATURE 3: KITCHEN QUEUE ----------------
def is_delayed(entry):
    return entry["status"] != "Ready" and minutes_since(entry["time"]) > entry["prep_time"] + DELAY_BUFFER


def view_queue():
    print("\n========== KITCHEN QUEUE ==========")
    if len(order_items) == 0:
        print("No orders in the queue.")
        return
    queue = sorted(order_items, key=lambda e: e["time"])   # oldest first
    print(f"{'ID':<5}{'Time':<10}{'Table':<7}{'Item':<20}{'Qty':<5}{'Waiting':<10}{'Status':<11}")
    for e in queue:
        flag = "  !! DELAYED" if is_delayed(e) else ""
        print(f"{e['id']:<5}{e['time'].strftime('%H:%M:%S'):<10}{e['table']:<7}"
              f"{e['name']:<20}{e['qty']:<5}{str(minutes_since(e['time'])) + ' min':<10}"
              f"{e['status']:<11}{flag}")


# ---------------- FEATURE 4: STATUS + WAITING TABLES ----------------
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


# ---------------- FEATURE 5: BILLING ----------------
def generate_bill():
    print("\n========== GENERATE TABLE BILL ==========")
    if len(order_items) == 0:
        print("No active orders.")
        return
    table = get_int("Enter table number: ", minimum=1)
    items = [e for e in order_items if e["table"] == table]
    if not items:
        print(f"\nNo orders found for Table {table}.")
        return

    not_ready = [e for e in items if e["status"] != "Ready"]
    if not_ready:
        print(f"\nWarning: {len(not_ready)} item(s) for this table are not ready yet.")
        if input("Generate bill anyway? (y/n): ").strip().lower() != "y":
            return

    # merge same items into one bill line
    lines = {}
    for e in items:
        if e["name"] not in lines:
            lines[e["name"]] = {"qty": 0, "price": e["price"]}
        lines[e["name"]]["qty"] += e["qty"]

    subtotal = 0
    print(f"\n----------- BILL: TABLE {table} -----------")
    print(f"{'Item':<20}{'Qty':>5}{'Price':>10}{'Amount':>12}")
    for name, line in lines.items():
        amount = line["qty"] * line["price"]
        subtotal += amount
        print(f"{name:<20}{line['qty']:>5}{line['price']:>10.2f}{amount:>12.2f}")
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    print("-" * 47)
    print(f"{'Subtotal':<35}{subtotal:>12.2f}")
    print(f"{'Tax (' + str(int(TAX_RATE * 100)) + '%)':<35}{tax:>12.2f}")
    print(f"{'TOTAL':<35}{total:>12.2f}")

    people = get_int("\nSplit bill between how many people? (1 for no split): ", minimum=1)
    if people > 1:
        print(f"Each person pays: Rs. {total / people:.2f}  (total split into {people} equal parts)")

    # table is settled: remove its items from the active queue
    order_items[:] = [e for e in order_items if e["table"] != table]
    print(f"\nTable {table} is now cleared. Thank you!")


# ---------------- STRETCH: BEST SELLERS ----------------
def best_sellers():
    print("\n========== TODAY'S BEST-SELLING ITEMS ==========")
    if not sales:
        print("No sales yet today.")
        return
    ranking = sorted(sales.items(), key=lambda pair: pair[1], reverse=True)
    for rank, (name, qty) in enumerate(ranking[:5], start=1):
        print(f"{rank}. {name} - {qty} sold")


# ---------------- MAIN ----------------
print("======================================")
print("              KITCHENSYNC")
print("     Restaurant Order Management")
print("======================================")

while True:
    print("\n========== MAIN MENU ==========")
    print("1. Manage Menu")
    print("2. Take New Order")
    print("3. View Kitchen Queue")
    print("4. Update Item Status")
    print("5. Generate Table Bill")
    print("6. Today's Best-Selling Items")
    print("7. Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        manage_menu()
    elif choice == "2":
        take_order()
    elif choice == "3":
        view_queue()
    elif choice == "4":
        status_menu()
    elif choice == "5":
        generate_bill()
    elif choice == "6":
        best_sellers()
    elif choice == "7":
        print("\nThank you for using KitchenSync!")
        break
    else:
        print("\nInvalid choice! Please enter a number between 1 and 7.")
