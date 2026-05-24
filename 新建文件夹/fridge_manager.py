from food import Food
from rules import get_default_expiry, calculate_food_nutrition, UNIT_RULES, category_options, recipes

# helper functions
def get_valid_name(prompt):
    while True:
        name = input(prompt + " (or 0 to cancel): ").strip().lower()
        if name == "0":
            return "0"
        if name != "":
            return name
        print("🚨 Input cannot be empty!")

def get_valid_quantity(quantity):
    while True:
        value = input(quantity).strip()
        try:
            value = float(value)
            if value <= 0:
                print("🚨 Please enter a number greater than 0.")
            else:
                return value
        except ValueError:
            print("🚨 Invalid input. Please enter a number.")

def get_unit_from_rules(food_name):
    food_name = food_name.lower()
    return UNIT_RULES.get(food_name)

def get_valid_unit(food_name):
    unit = get_unit_from_rules(food_name)

    if unit is not None:
        return unit

    while True:
        unit = input(f"Enter unit for {food_name} (g/L/pcs): ").strip()

        if unit in ["g", "L", "pcs"]:
            return unit

        print("🚨 Invalid unit. Please enter g, L, or pcs.")

def get_valid_location():
    while True:
        location = input("Enter location (fridge/freezer): ").strip().lower()
        if location == "fridge" or location == "freezer":
            return location
        print("🚨 Invalid location. Please enter fridge or freezer.")

def get_valid_category():
    while True:
        print("\nChoose category:")
        print("1. Dairy")
        print("2. Meat")
        print("3. Seafood")
        print("4. Vegetable")
        print("5. Fruit")
        print("6. Other")
        choice = input("Choose category number: ")
        if choice in category_options:
            return category_options[choice]
        print("🚨 Invalid choice. Please try again.")

def get_valid_expiry_date():
    while True:
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
        try:
            days_left = Food.calculate_expiry_days(expiry_date)
            if days_left < 0:
                print("🚨 Expiry date cannot be in the past.")
            else:
                return days_left
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")

# Inventory class
class Inventory:
    def __init__(self):
        self.inventory = []
        self.expired_inventory = []

    def load_inventory_data(self, username):
        self.username = username
        self.inventory = []
        self.expired_inventory = []
        try:
            with open(f"saves/{self.username}_inventory.txt", "r") as file:
                while True:
                    line = file.readline()
                    if line == "":
                        break
                    food = Food.from_file_line(line)
                    if food is not None:
                        self.inventory.append(food)
        except FileNotFoundError:
            print(f"📦 No saved inventory data found for {self.username}. Starting with an empty inventory.")
        try:
            with open(f"saves/{self.username}_expired_inventory.txt", "r") as file:
                while True:
                    line = file.readline()
                    if line == "":
                        break
                    food = Food.from_file_line(line)
                    if food is not None:
                        self.expired_inventory.append(food)
        except FileNotFoundError:
            print("⚫ No expired inventory found.")

    def save_inventory_data(self):
        with open(f"saves/{self.username}_inventory.txt", "w") as file:
            for food in self.inventory:
                file.write(food.to_file_line() + "\n")

        with open(f"saves/{self.username}_expired_inventory.txt", "w") as file:
            for food in self.expired_inventory:
                file.write(food.to_file_line() + "\n")

    def update_expiry_after_login(self, days_passed):
        if days_passed <= 0:
            return

        print("\n===== ⏰ Automatic Time Progress =====")
        print(f"📅 Days passed: {days_passed}")

        for food in self.inventory:
            food.reduce_expired_days(days_passed)
            print(f"{Food.get_icon(food.name)} {food.name.title()} now has {food.current_expiry_days} days left")

        self.move_expired_inventory()
        self.save_inventory_data()

    def move_expired_inventory(self):
        still_good_food = []

        for food in self.inventory:
            if food.is_expired():
                self.expired_inventory.append(food)
                print(f"⚫ {food.name.title()} has expired and was moved to expired inventory.")
            else:
                still_good_food.append(food)

        self.inventory = still_good_food

    def view_inventory(self):
        if len(self.inventory) == 0:
            print("\n📦 Inventory is empty.")
            return

        print("\n===== 📦 Inventory =====")

        food_batches = {}
        for food in self.inventory:
            if food.name not in food_batches:
                food_batches[food.name] = []
            food_batches[food.name].append(food)

        for name in food_batches:
            food_batches[name].sort(key=lambda x: x.current_expiry_days)

        sorted_names = sorted(
            food_batches.keys(),
            key=lambda name: min(
                food.current_expiry_days
                for food in food_batches[name]
            )
        )

        for name in sorted_names:
            batches = food_batches[name]
            total = 0
            for food in batches:
                total += food.quantity
            print(f"\n{Food.get_icon(name)} {name.title()}: total {total:g}{food.unit}")
            for i, food in enumerate(batches, start=1):
                print(f"• {i}: {food.quantity:g} {food.unit} | {food.location} | {food.get_food_status()}")

    def view_categories(self):
        print("\n===== Food Categories =====")
        if len(self.inventory) == 0:
            print("📦 Inventory is empty.")
            return

        categories = {}

        for food in self.inventory:
            category = food.category
            if category not in categories:
                categories[category] = []
            if food.name not in categories[category]:
                categories[category].append(food.name)

        for category in categories:
            print(f"\n{category.title()}")
            for name in categories[category]:
                print(f"{Food.get_icon(name)} {name.title()}")

    def add_food(self):
        print("\n===== ➕ Add Food =====")
        name = get_valid_name("Enter food name: ")
        if name == "0":
            print("↩️ Add food cancelled.")
            return
        unit = get_valid_unit(name)
        quantity = get_valid_quantity(f"Enter quantity ({unit}): ")
        category = get_valid_category()
        location = get_valid_location()
        default_expiry = get_default_expiry(name, location)

        if default_expiry is not None:
            print(f"\nExpiry detected automatically: {default_expiry} days")
            print("Use default expiry date?")
            print("1. Yes")
            print("2. Set custom expiry date")

            while True:
                choice = input("Choose: ")
                if choice == "1":
                    current_expiry_days = default_expiry
                    original_expiry_days = default_expiry
                    break

                elif choice == "2":
                    current_expiry_days = get_valid_expiry_date()
                    original_expiry_days = current_expiry_days
                    break
                else:
                    print("🚨 Invalid choice. Please enter 1 or 2.")

        else:
            print("\n⚠️ No expiry rule found for this food.")
            current_expiry_days = get_valid_expiry_date()
            original_expiry_days = current_expiry_days

        food = Food(name, quantity, unit, category, location, current_expiry_days, original_expiry_days)
        self.inventory.append(food)
        print(f"✅ {Food.get_icon(name)} {name.title()} added successfully.")
        self.save_inventory_data()


    def use_food(self, user):
        print("\n===== 🍽️ Use Food 🍽️ =====")

        name = get_valid_name("Enter food name to use: ")
        if name == "0":
            print("↩️ Add food cancelled.")
            return
        unit = get_valid_unit(name)
        quantity_reduced = get_valid_quantity(f"Enter quantity to use ({unit}): ")

        nutrition = self.reduce_food_from_inventory(name, quantity_reduced, action="Used", add_nutrition=True)

        if nutrition is not None:
            user.add_intake(nutrition)
            print("\nNutrition Added:")
            print(f"🔥 Calories: {nutrition['calories']:.1f} kcal")
            print(f"💪 Protein: {nutrition['protein']:.1f} g")
            print(f"🍚 Carbs: {nutrition['carbs']:.1f} g")
        self.save_inventory_data()

    def remove_food(self):
        print("\n===== 🚮 Remove Food =====")
        name = get_valid_name("Enter food name to remove: ")
        if name == "0":
            print("↩️ Add food cancelled.")
            return
        unit = get_valid_unit(name)
        quantity_reduced = get_valid_quantity(f"Enter quantity to remove ({unit}): ")
        self.reduce_food_from_inventory(name, quantity_reduced, action="Removed", add_nutrition=False)
        self.save_inventory_data()

    def reduce_food_from_inventory(self, name, quantity_reduced, action="Used", add_nutrition=True):
        matching = []

        for food in self.inventory:
            if food.name == name:
                matching.append(food)

        if len(matching) == 0:
            print("🚨 Food not found.")
            return None

        total_available = 0

        for food in matching:
            total_available += food.quantity

        if total_available < quantity_reduced:
            print(f"🚨 Not enough {name}. Available: {total_available:g}{matching[0].unit}")
            return None

        matching.sort(key=lambda x: x.current_expiry_days)

        quantity_remaining_to_reduce = quantity_reduced
        total_nutrition = {"calories": 0, "protein": 0, "carbs": 0}

        print(f"\n{action}:")

        for food in matching:
            if quantity_remaining_to_reduce <= 0:
                break

            reduced_quantity = food.reduce_quantity(quantity_remaining_to_reduce)
            quantity_remaining_to_reduce -= reduced_quantity

            print(f"{food.name.title()} {reduced_quantity:g}{food.unit} {action.lower()} ({food.current_expiry_days} days left)")

            if add_nutrition:
                n = calculate_food_nutrition(name, reduced_quantity, food.unit)
                total_nutrition["calories"] += n["calories"]
                total_nutrition["protein"] += n["protein"]
                total_nutrition["carbs"] += n["carbs"]

        new_inventory = []
        for food in self.inventory:
            if not food.is_empty():
                new_inventory.append(food)

        self.inventory = new_inventory

        if add_nutrition:
            return total_nutrition
        return None

    def view_expired_inventory(self):
        if len(self.expired_inventory) == 0:
            print("\n⚫ No expired items.")
            return

        print("\n===== ⚫ Expired Items =====")

        for food in self.expired_inventory:
            print(food.display_one_line())

    def clear_expired_inventory(self):
        self.expired_inventory = []
        print("🧹 Expired items removed successfully.")
        self.save_inventory_data()


# Recipe Functions
def calculate_recipe_nutrition(recipe_name):
    recipe = recipes[recipe_name]
    total = {"calories": 0, "protein": 0, "carbs": 0}

    for food_name, quantity in recipe.items():
        unit = get_valid_unit(food_name)
        n = calculate_food_nutrition(food_name, quantity, unit)

        total["calories"] += n["calories"]
        total["protein"] += n["protein"]
        total["carbs"] += n["carbs"]

    return total


def has_enough_ingredients(inventory, recipe_name):
    recipe = recipes[recipe_name]

    for food_name, quantity in recipe.items():
        available = 0

        for food in inventory.inventory:
            if food.name == food_name:
                available += food.quantity

        if available < quantity:
            return False
    return True


def recommend_recipe(inventory, user):
    print("\n===== 🍳 Recipe Recommendation =====")

    suitable_recipes = []

    for recipe_name in recipes:
        if has_enough_ingredients(inventory, recipe_name):
            nutrition = calculate_recipe_nutrition(recipe_name)
            if user.goal == "No Goal":
                suitable_recipes.append((recipe_name, nutrition))
            else:
                if user.recipe_matches_goal(nutrition):
                    suitable_recipes.append((recipe_name, nutrition))

    if len(suitable_recipes) == 0:
        print("❌ No suitable recipe found.")
        return

    print(f"🎯 Goal: {user.goal}")

    for i, item in enumerate(suitable_recipes, start=1):
        recipe_name = item[0]
        nutrition = item[1]

        print(f"{i}. {recipe_name}: 🔥 {nutrition['calories']:.1f} kcal, 💪 {nutrition['protein']:.1f}g protein, 🍚 {nutrition['carbs']:.1f}g carbs")


def cook_recipe(inventory, user):
    print("\n===== 👨‍🍳 Smart Recipe Cooking =====")

    ready_to_cook_recipes = []

    for recipe_name in recipes:
        if has_enough_ingredients(inventory, recipe_name):
            ready_to_cook_recipes.append(recipe_name)

    if len(ready_to_cook_recipes) == 0:
        print("❌ No recipe can be cooked with current inventory.")
        return

    for i, recipe_name in enumerate(ready_to_cook_recipes, start=1):
        print(f"{i}. {recipe_name}")

    while True:
        choice = input("Choose recipe to cook (0 to cancel): ")
        if choice == "0":
            print("↩️ Cooking cancelled.")
            return
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(ready_to_cook_recipes):
                break
        print("❌ Invalid choice. Please enter a valid recipe number.")

    recipe_name = ready_to_cook_recipes[index]
    recipe = recipes[recipe_name]

    total_nutrition = {"calories": 0, "protein": 0, "carbs": 0}
    print(f"\nCooked: {recipe_name}")

    for food_name, amount in recipe.items():
        nutrition = inventory.reduce_food_from_inventory(food_name, amount, action="Used", add_nutrition=True)

        if nutrition is not None:
            total_nutrition["calories"] += nutrition["calories"]
            total_nutrition["protein"] += nutrition["protein"]
            total_nutrition["carbs"] += nutrition["carbs"]

    user.add_intake(total_nutrition)

    print("\nNutrition Added:")
    print(f"🔥 Calories: {total_nutrition['calories']:.1f} kcal")
    print(f"💪 Protein: {total_nutrition['protein']:.1f} g")
    print(f"🍚 Carbs: {total_nutrition['carbs']:.1f} g")
    inventory.save_inventory_data()
