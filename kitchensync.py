# Configuration and settings
from config import (
    TAX_RATE,
    DELAY_BUFFER,
    MAX_NAME_LEN,
    MAX_PRICE,
    MAX_PREP_TIME,
    MAX_QTY,
    MAX_TABLE,
    MAX_PEOPLE,
)

# Shared data structures
import data
from data import (
    menu,
    order_items,
    sales,
    next_order_id,
)

# Utility and helper functions
from utils import (
    get_text,
    get_int,
    get_float,
    minutes_since,
)

# Feature modules
from menu_manager import (
    find_menu_item,
    show_menu,
    manage_menu,
)
from order_manager import take_order
from kitchen_queue import (
    is_delayed,
    view_queue,
    show_waiting_tables,
    update_status,
    status_menu,
)
from billing import generate_bill
from analytics import best_sellers


def main():
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


if __name__ == "__main__":
    main()
