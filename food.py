from datetime import date
from rules import ICON_RULES

class Food:
    def __init__(self, name, quantity, unit, category, location, current_expiry_days, original_expiry_days):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.category = category
        self.location = location
        self.current_expiry_days = current_expiry_days
        self.original_expiry_days = original_expiry_days

    def get_food_status(self):
        if self.current_expiry_days < 0:
            return "⚫ Expired"
        elif self.current_expiry_days == 0:
            return "🔴 TODAY"
        elif self.current_expiry_days <= 3:
            return f"🟡 {self.current_expiry_days} days left"
        else:
            return f"🟢 {self.current_expiry_days} days left"

    def reduce_expired_days(self, days_passed):
        self.current_expiry_days -= days_passed

    def is_expired(self):
        return self.current_expiry_days < 0

    def reduce_quantity(self, quantity_remaining_to_reduce):
        if self.quantity <= quantity_remaining_to_reduce:
            reduced_quantity = self.quantity
            self.quantity = 0
        else:
            reduced_quantity = quantity_remaining_to_reduce
            self.quantity -= quantity_remaining_to_reduce

        return reduced_quantity

    def is_empty(self):
        return self.quantity <= 0

    def to_file_line(self):
        return f"{self.name}|{self.quantity}|{self.unit}|{self.category}|{self.location}|{self.current_expiry_days}|{self.original_expiry_days}"

    def display_one_line(self):
        return f"{Food.get_icon(self.name)} {self.name.title()} | {self.get_food_status()} | {self.quantity:g}{self.unit} | {self.location}"

    @staticmethod
    def get_icon(food_name):
        return ICON_RULES.get(food_name.lower(), "🍽️")

    @staticmethod
    def calculate_expiry_days(expiry_date):
        expiry_date = date.fromisoformat(expiry_date)
        today = date.today()
        return (expiry_date - today).days

    @staticmethod
    def from_file_line(line):
        parts = line.strip().split("|")
        if len(parts) != 7:
            return None
        return Food(parts[0], float(parts[1]), parts[2], parts[3], parts[4], int(parts[5]), int(parts[6]))

