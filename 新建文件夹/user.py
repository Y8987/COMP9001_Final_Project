from datetime import date
from rules import goal_ranges


class User:
    def __init__(self, username):
        self.username = username
        self.password = ""
        self.goal = "No Goal"
        self.last_login = str(date.today())
        self.intake_date = str(date.today())
        self.today_calories = 0
        self.today_protein = 0
        self.today_carbs = 0

    def authenticate(self):
        if self.password == "":
            print("\n🆕 New user detected.")
            self.password = input("Create password: ")
            self.save()
            print("✅ Password created.")
            return

        while True:
            password = input("Enter password: ")
            if password == self.password:
                print("✅ Login successful.")
                break
            print("❌ Wrong password.")

    def choose_goal(self):
        while True:
            print("\n------ 🎯Health Goal ------")
            print("💪 1. Muscle Gain")
            print("🔥 2. Fat Loss")
            print("🍭 3. Low Sugar")
            print("💭 4. No Goal")

            choice = input("Choose your health goal: ")

            if choice == '1':
                self.goal = "Muscle Gain"
                break
            elif choice == '2':
                self.goal = "Fat Loss"
                break
            elif choice == '3':
                self.goal = "Low Sugar"
                break
            elif choice == '4':
                self.goal = "No Goal"
                break
            else:
                print("Invalid choice")
                continue

        self.save()
        print(f"🎯Health goal set to: {self.goal}")

    def add_intake(self, nutrition):
        self.today_calories += nutrition["calories"]
        self.today_protein += nutrition["protein"]
        self.today_carbs += nutrition["carbs"]
        self.save()

    def show_intake(self):
        print("\n===== 📊 Today's Intake =====")
        print(f"🔥 Calories: {self.today_calories:.1f} kcal")
        print(f"💪 Protein: {self.today_protein:.1f} g")
        print(f"🍚 Carbs: {self.today_carbs:.1f} g")
        print(f"🎯 Goal: {self.goal}")

    def recipe_matches_goal(self, nutrition):
        if self.goal == "No Goal":
            return True

        goal = goal_ranges[self.goal]
        for nutrient in goal:
            min_value = goal[nutrient][0]
            max_value = goal[nutrient][1]
            if nutrition[nutrient] < min_value:
                return False
            if nutrition[nutrient] > max_value:
                return False
        return True

    def reset_intake_if_new_day(self):

        today = str(date.today())

        if self.intake_date != today:
            self.intake_date = today
            self.today_calories = 0
            self.today_protein = 0
            self.today_carbs = 0
            self.save()

    def get_days_passed(self):
        old_date = date.fromisoformat(self.last_login)
        today = date.today()
        return (today - old_date).days

    def update_last_login(self):
        self.last_login = str(date.today())
        self.save()

    def show_profile(self):
        print("\n===== 🪪User Profile =====")
        print(f"Username: {self.username}")
        print(f"Health Goal: {self.goal}")
        print(f"Last Login: {self.last_login}")

    def load(self):
        try:
            with (open(f"saves/{self.username}_profile.txt", "r") as file):
                for line in file:
                    line = line.strip()
                    if line.startswith("username: "):
                        self.password = line.replace("username: ", "")
                    elif line.startswith("password: "):
                        self.password = line.replace("password: ", "")
                    elif line.startswith("goal: "):
                        self.goal = line.replace("goal: ", "")
                    elif line.startswith("last_login: "):
                        self.last_login = line.replace("last_login: ", "")
                    elif line.startswith("intake_date: "):
                        self.intake_date = line.replace("intake_date: ", "")
                    elif line.startswith("calories: "):
                        self.today_calories = float(line.replace("calories: ", ""))
                    elif line.startswith("protein: "):
                        self.today_protein = float(line.replace("protein: ", ""))
                    elif line.startswith("carbs: "):
                        self.today_carbs = float(line.replace("carbs: ", ""))
        except FileNotFoundError:
            self.save()
        self.reset_intake_if_new_day()

    def save(self):
        with open(f"saves/{self.username}_profile.txt", "w") as file:
            file.write(f"username: {self.username}\n")
            file.write(f"password: {self.password}\n")
            file.write(f"goal: {self.goal}\n")
            file.write(f"last_login: {self.last_login}\n")
            file.write(f"intake_date: {self.intake_date}\n")
            file.write(f"calories: {self.today_calories}\n")
            file.write(f"protein: {self.today_protein}\n")
            file.write(f"carbs: {self.today_carbs}\n")



