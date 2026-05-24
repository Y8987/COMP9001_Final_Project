# Run this file to start the program:
# python main.py

# FridgeAssistant 
#
# To run the program:
# 1. Open terminal
# 2. Navigate to the project folder:
#    cd FridgeAssistant
# 3. Run:
#    python main.py

from user import User
from fridge_manager import Inventory, recommend_recipe, cook_recipe

def main_menu():
    print("\n===== Main Menu =====")
    print("📦 1. View Inventory")
    print("➕ 2. Add Food")
    print("🍽️ 3. Use Food")
    print("🗑️ 4. Remove Food")
    print("⚫ 5. View Expired Items")
    print("🧹 6. Clear Expired Items")
    print("📂 7. View Categories")
    print("🎯 8. Set Health Goal")
    print("🍳 9. Recommend Recipe")
    print("👨‍🍳 10. Cook Recipe")
    print("📊 11. View Today's Intake")
    print("👤 12. View User Profile")
    print("🚪 0. Exit")


def main():
    print("===== 🧊 Smart Fridge Pro =====")
    while True:
        username = input("Enter username: ").strip()
        if username != "":
            break
        print("❌ Invalid username. Please enter something.")
    user = User(username)
    user.load()
    user.authenticate()

    inventory = Inventory()
    inventory.load_inventory_data(username)

    days_passed = user.get_days_passed()

    if days_passed > 0:
        inventory.update_expiry_after_login(days_passed)
    user.update_last_login()

    while True:
        main_menu()

        choice = input("Choose: ")

        if choice == "1":
            inventory.view_inventory()

        elif choice == "2":
            inventory.add_food()

        elif choice == "3":
            inventory.use_food(user)

        elif choice == "4":
            inventory.remove_food()

        elif choice == "5":
            inventory.view_expired_inventory()

        elif choice == "6":
            inventory.clear_expired_inventory()

        elif choice == "7":
            inventory.view_categories()

        elif choice == "8":
            user.choose_goal()

        elif choice == "9":
            recommend_recipe(inventory, user)

        elif choice == "10":
            cook_recipe(inventory, user)

        elif choice == "11":
            user.show_intake()

        elif choice == "12":
            user.show_profile()

        elif choice == "0":
            user.save()
            print("👋🏻 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
