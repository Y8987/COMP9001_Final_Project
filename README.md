# FridgeAssistant

FridgeAssistant is a terminal-based object-oriented fridge management system.  
It helps users record and organize food, reducing food waste and unnecessary repeated purchases.

The system automatically updates food expiry days based on the number of days passed since the user's last login. Expired food items are moved to a separate expired inventory section to remind users to clean their fridge in time. Users can also view freshness status indicators to identify food that is close to expiring.

In addition, FridgeAssistant recommends recipes based on the current inventory and supports health goals such as Muscle Gain, Fat Loss, and Low Sugar. The system also includes daily nutrition intake tracking to help users manage their eating habits more effectively.

---

# Main Features

- User login and profile system
- Food information recording
- Fridge inventory management, including adding, using, and removing food
- Inventory display grouped by food categories and sorted by remaining expiry days
- Automatic expiry updates after login and automatic movement of expired food into the expired inventory section
- Food category viewing
- Health goal selection
- Recipe recommendation
- Recipe recommendation based on current inventory when no health goal is selected
- Goal-based recipe recommendation according to the selected health goal
- Recipe cooking
- Daily calorie, protein, and carbohydrate intake tracking
- Save and load data

---

# Project Files

## `main.py`
The entry point of the program. It displays the main menu, receives user input, and controls the overall program flow.

## `food.py`
Contains the Food class, which stores food item information and handles food status, expiry-related methods, and other related functions.

## `fridge_manager.py`
Contains the Inventory class and inventory management features.  
It also includes recipe recommendation, recipe cooking, nutrition calculation, and input helper functions.

## `user.py`
Contains the User class. Manages user login information, health goals, and nutrition intake tracking.

## `rules.py`
Stores system rule data and rule-based helper functions.

---

# How to Run

Run the following command in terminal:

```bash
python main.py
```

---

# Save Files

The program stores user data inside the `saves` folder.  
For each user, the system creates files such as:

- `username_profile.txt`
- `username_inventory.txt`
- `username_expired_inventory.txt`

---

# Technologies Used

- Object-Oriented Programming (OOP)
- Terminal-Based Application
