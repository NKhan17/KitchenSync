from config import MAX_NAME_LEN, MAX_PRICE, MAX_PREP_TIME
from data import menu
from utils import get_text, get_int, get_float


def find_menu_item(name):
    for item in menu:
        if item["name"].lower() == name.lower():
            return item
    return None


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
            elif len(name) > MAX_NAME_LEN:
                print(f"\nFood name is too long! Maximum {MAX_NAME_LEN} characters.")
            elif find_menu_item(name):
                print("\nThat item is already on the menu!")
            else:
                price = get_float("Enter price: ", maximum=MAX_PRICE)
                prep_time = get_int("Enter preparation time (minutes): ",
                                    minimum=1, maximum=MAX_PREP_TIME)
                menu.append({"name": name, "price": price, "prep_time": prep_time})
                print("\nFood item added successfully!")

        elif choice == "2":
            show_menu()

        elif choice == "3":
            break

        else:
            print("\nInvalid choice!")
