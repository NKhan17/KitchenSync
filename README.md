# KitchenSync: Restaurant Order Routing and Kitchen Display System

A menu-driven **console application in Python** that helps a restaurant send orders from tables to the kitchen, track item status, and bill tables. It replaces shouting orders to the kitchen, where items get missed or delayed.

**Problem statement:** CP-061 (Food, Hospitality and Events, Intermediate)

## Features

### Core features
1. **Maintain the menu** with price and preparation time
2. **Take orders per table** with items and quantities
3. **Kitchen queue** shown in order-time sequence with each item's status
4. **Mark items ready** (Pending, Preparing, Ready) and **show waiting tables**
5. **Table bill** with 5% tax and an equal split between people

### Stretch features
- **Delay flag:** items waiting longer than their preparation time + 10 minutes are marked `!! DELAYED`
- **Best sellers:** shows the day's top-selling items

## How to run

Requires **Python 3.6 or later**. No extra libraries or database are needed.

```
python kitchensync.py
```

## Quick walkthrough

1. **Manage Menu**, then **Add Food Item**: add a few dishes with a price and prep time.
2. **Take New Order**: enter a table number, pick items by their menu number, and give quantities. Enter `0` to finish.
3. **View Kitchen Queue**: see all items oldest first, with status and waiting time.
4. **Update Item Status**: set an item to *Preparing* or *Ready*, or view tables still waiting.
5. **Generate Table Bill**: see the itemised bill with tax, optionally split it between people. The table is then cleared.
6. **Today's Best-Selling Items**: see the ranking.
7. **Exit**

## Input validation

All input is checked, and the program asks again instead of crashing.

| Input | Rule |
|---|---|
| Food name | Not empty, at most 20 characters, no duplicates (case-insensitive) |
| Price | A valid number, above 0, at most Rs. 10,000 (NaN and infinity rejected) |
| Prep time | Whole number, 1 to 180 minutes |
| Table number | Whole number, 1 to 100 |
| Quantity | Whole number, 1 to 50 per line |
| Split | Whole number, 1 to 20 people |
| Menu choices | Anything outside the listed options shows "Invalid choice" |

The limits are constants at the top of `kitchensync.py` and can be changed in one place.

## How it works

- **Data storage:** everything is kept in memory using Python lists and dicts. Data is lost when the program closes (no database, as per the brief).
  - `menu`: list of dicts (`name`, `price`, `prep_time`)
  - `order_items`: list of dicts, one per ordered line. This is the kitchen queue.
  - `sales`: dict of item name to total quantity sold
- **Order queue:** each ordered line is stamped with `datetime.now()` and the queue is displayed sorted by that time (oldest first).
- **Status tracking:** each item has a `status` field that moves Pending, then Preparing, then Ready.
- **Delay check:** an item is delayed if it isn't Ready and `minutes waited > prep time + 10`.
- **Billing:** identical items are merged into one line. Tax and total are rounded to 2 decimals so the printed lines add up exactly.
- **Equal split:** the total is converted to paise (whole numbers) and divided, with leftover paise given one each to the first few people. The shares always add up to the exact bill total (e.g. Rs. 350.00 between 3 people is 116.67 + 116.67 + 116.66).

## Settings

Edit these constants at the top of `kitchensync.py`:

```python
TAX_RATE = 0.05        # 5% GST
DELAY_BUFFER = 10      # extra minutes before an item is flagged as delayed
```

**Tip for testing the delay flag:** set `DELAY_BUFFER = -1`, place an order, wait about a minute, and view the queue. Remember to set it back to `10`.

## Project structure

```
kitchensync.py   # the entire application
README.md        # this file
```

## Team

- Neha Khan - 1AT24CS138
- Naznin A - 1AT24CS136
