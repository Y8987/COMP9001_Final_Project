ICON_RULES = {
    "milk": "🥛",
    "cheese": "🧀",
    "butter": "🧈",
    "chicken": "🍗",
    "beef": "🥩",
    "bacon": "🥓",
    "lamb": "🍖",
    "fish": "🐟",
    "shrimp": "🍤",
    "carrot": "🥕",
    "broccoli": "🥦",
    "cucumber": "🥒",
    "potato": "🥔",
    "mushroom": "🍄",
    "tomato": "🍅",
    "banana": "🍌",
    "egg": "🥚",
    "bread": "🍞"
}

# Store default measurement units for each food
UNIT_RULES = {
    "milk": "L",
    "cheese": "g",
    "butter": "g",
    "chicken": "g",
    "beef": "g",
    "bacon": "g",
    "lamb": "g",
    "fish": "g",
    "shrimp": "g",
    "broccoli": "g",
    "carrot": "pcs",
    "cucumber": "pcs",
    "potato": "pcs",
    "mushroom": "pcs",
    "tomato": "pcs",
    "banana": "pcs",
    "egg": "pcs",
    "bread": "pcs"
}
# Store default expiry days based on food type and storage location
expiry_rules = {
    ("milk", "fridge"): 7,
    ("cheese", "fridge"): 14,
    ("butter", "fridge"): 30,
    ("chicken", "fridge"): 3,
    ("chicken", "freezer"): 20,
    ("beef", "fridge"): 3,
    ("beef", "freezer"): 20,
    ("bacon", "fridge"): 7,
    ("lamb", "fridge"): 3,
    ("lamb", "freezer"): 20,
    ("fish", "fridge"): 2,
    ("fish", "freezer"): 15,
    ("shrimp", "fridge"): 2,
    ("shrimp", "freezer"): 15,
    ("broccoli", "fridge"): 7,
    ("carrot", "fridge"): 7,
    ("cucumber", "fridge"): 7,
    ("potato", "fridge"): 7,
    ("mushroom", "fridge"): 3,
    ("tomato", "fridge"): 3,
    ("banana", "fridge"): 3,
    ("egg", "fridge"): 14,
    ("bread", "fridge"): 3
}

# Food measured in grams (g) use nutrition values per 100g
# Food measured in litres (L) use nutrition values per 1L
# Food measured in pieces (pcs) use nutrition values per 1 piece
# Store nutrition data for each food item
nutrition_per_unit = {
    "milk": {"calories": 600, "protein": 32, "carbs": 48},
    "cheese": {"calories": 400, "protein": 25, "carbs": 1},
    "butter": {"calories": 717, "protein": 1, "carbs": 0},
    "chicken": {"calories": 165, "protein": 31, "carbs": 0},
    "beef": {"calories": 250, "protein": 26, "carbs": 0},
    "bacon": {"calories": 541, "protein": 37, "carbs": 1},
    "lamb": {"calories": 294, "protein": 25, "carbs": 0},
    "fish": {"calories": 206, "protein": 22, "carbs": 0},
    "shrimp": {"calories": 99, "protein": 24, "carbs": 0},
    "broccoli": {"calories": 35, "protein": 2.5, "carbs": 7},
    "carrot": {"calories": 25, "protein": 0.5, "carbs": 6},
    "cucumber": {"calories": 16, "protein": 0.7, "carbs": 4},
    "potato": {"calories": 77, "protein": 2, "carbs": 17},
    "mushroom": {"calories": 22, "protein": 3, "carbs": 3},
    "tomato": {"calories": 22, "protein": 1, "carbs": 5},
    "banana": {"calories": 105, "protein": 1.3, "carbs": 27},
    "egg": {"calories": 70, "protein": 6, "carbs": 1},
    "bread": {"calories": 80, "protein": 3, "carbs": 15}
}

# Store recipe ingredients and required quantities
recipes = {
    "Chicken Sandwich": {"chicken": 150, "bread": 2, "tomato": 1},
    "Egg Sandwich": {"egg": 2, "bread": 2},
    "Beef with Potato": {"beef": 300, "potato": 2},
    "Fried Shrimp": {"shrimp": 150, "butter": 15},
    "Milk Banana": {"milk": 0.5, "banana": 1},
    "Broccoli Mushroom Stir Fry": {"broccoli": 100, "mushroom": 3}
}

category_options = {
    "1": "dairy",
    "2": "meat",
    "3": "seafood",
    "4": "vegetable",
    "5": "fruit",
    "6": "other"
}

# Recommend nutrition ranges per meal
goal_ranges = {
    "Muscle Gain": {"calories": (400, 800), "protein": (30, 80), "carbs": (20, 100)},
    "Fat Loss": {"calories": (200, 500), "protein": (20, 60), "carbs": (0, 50)},
    "Low Sugar": {"calories": (200, 600), "protein": (10, 70), "carbs": (0, 30)}
}

def get_default_expiry(food_name, location):
    return expiry_rules.get((food_name.lower(), location.lower()))

def calculate_food_nutrition(food_name, quantity, unit):
    food_name = food_name.lower()
    if food_name not in nutrition_per_unit:
        print("⚠️ Nutrition data not found.")
        return None
    if unit == "g":
        multiplier = quantity / 100
    else:
        multiplier = quantity
    return {"calories": nutrition_per_unit[food_name]["calories"] * multiplier, "protein": nutrition_per_unit[food_name]["protein"] * multiplier, "carbs": nutrition_per_unit[food_name]["carbs"] * multiplier}



