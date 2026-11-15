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

