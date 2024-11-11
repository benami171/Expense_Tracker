# main.py
from SpendingManager import SpendingManager
from datetime import datetime

def display_menu():
    print("\n--- Spending Manager ---")
    print("1. View current month's spending statistics")
    print("2. Add a new spending")
    print("3. Exit")

def get_current_month_statistics(manager):
    current_date = datetime.now()
    monthly_summary = manager.get_monthly_summary(current_date.year, current_date.month)
    total_spent = sum(monthly_summary.values())
    average_spending = total_spent / current_date.day if current_date.day > 0 else 0

    print("\n--- Current Month's Spending Statistics ---")
    print(f"Total spent this month: ${total_spent:.2f}")
    print(f"Average spending per day: ${average_spending:.2f}")
    print("\nSpending amount per category:")
    print(f"{'Category':<30} {'Amount':<10}")  # Table header
    print("-" * 40)  # Separator
    for category, amount in monthly_summary.items():
        print(f"{category:<30} ${amount:<10.2f}")  # Table rows

def choose_category():
    categories = [
        "Housing",
        "Utilities",
        "Groceries",
        "Transportation",
        "Healthcare",
        "Entertainment",
        "Personal Care",
        "Clothing & Accessories",
        "Savings & Investments",
        "Gifts",
        "Education",
        "Other"
    ]
    
    print("\nChoose a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")
    
    choice = int(input("Enter the category number: "))
    if 1 <= choice <= len(categories):
        return categories[choice - 1]
    else:
        print("Invalid choice. Defaulting to 'Other'")
        return "Other"

def add_new_spending(manager):
    amount = float(input("Enter the amount spent: "))
    purchaser = input("Enter the purchaser's name: ")
    category = choose_category()  # Use the new category selection function
    shop_name = input("Enter the shop name (optional): ")
    description = input("What did you buy? (description): ")
    manager.add_spending(amount, purchaser, category, shop_name, description)
    print("Spending added successfully!")

def main():
    manager = SpendingManager()

    while True:
        display_menu()
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            get_current_month_statistics(manager)
        elif choice == '2':
            add_new_spending(manager)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()