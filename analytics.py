from data import sales


def best_sellers():
    print("\n========== TODAY'S BEST-SELLING ITEMS ==========")
    if not sales:
        print("No sales yet today.")
        return
    ranking = sorted(sales.items(), key=lambda pair: pair[1], reverse=True)
    for rank, (name, qty) in enumerate(ranking[:5], start=1):
        print(f"{rank}. {name} - {qty} sold")
