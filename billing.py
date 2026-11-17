from config import TAX_RATE, MAX_TABLE, MAX_PEOPLE
from data import order_items
from utils import get_int


def generate_bill():
    print("\n========== GENERATE TABLE BILL ==========")
    if len(order_items) == 0:
        print("No active orders.")
        return
    table = get_int(f"Enter table number (1-{MAX_TABLE}): ", minimum=1, maximum=MAX_TABLE)
    items = [e for e in order_items if e["table"] == table]
    if not items:
        print(f"\nNo orders found for Table {table}.")
        return

    not_ready = [e for e in items if e["status"] != "Ready"]
    if not_ready:
        print(f"\nWarning: {len(not_ready)} item(s) for this table are not ready yet.")
        if input("Generate bill anyway? (y/n): ").strip().lower() != "y":
            return

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
    subtotal = round(subtotal, 2)
    tax = round(subtotal * TAX_RATE, 2)      
    total = round(subtotal + tax, 2)
    print("-" * 47)
    print(f"{'Subtotal':<35}{subtotal:>12.2f}")
    print(f"{'Tax (' + str(int(TAX_RATE * 100)) + '%)':<35}{tax:>12.2f}")
    print(f"{'TOTAL':<35}{total:>12.2f}")

    people = get_int(f"\nSplit bill between how many people? (1-{MAX_PEOPLE}, 1 for no split): ",
                     minimum=1, maximum=MAX_PEOPLE)
    if people > 1:
        total_paise = round(total * 100)
        base = total_paise // people         
        extra = total_paise % people          
        if extra == 0:
            print(f"Each person pays: Rs. {base / 100:.2f}")
        else:
            print(f"{extra} person(s) pay: Rs. {(base + 1) / 100:.2f}")
            print(f"{people - extra} person(s) pay: Rs. {base / 100:.2f}")
        print(f"(Shares add up to the exact total of Rs. {total:.2f})")

    order_items[:] = [e for e in order_items if e["table"] != table]
    print(f"\nTable {table} is now cleared. Thank you!")
