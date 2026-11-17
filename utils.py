import math
from datetime import datetime


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


def get_float(prompt, minimum=0, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not math.isfinite(number):
            print("Please enter a valid number.")
            continue
        
        if maximum is not None and number > maximum:
            print(f"Value must be at most {maximum}.")
            continue
        number = round(number, 2)         
        
        if number <= minimum:
            print(f"Value must be greater than {minimum}.")
        else:
            return number


def minutes_since(start):
    return int((datetime.now() - start).total_seconds() // 60)
