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
    print("Spending amount per category:")
    for category, amount in monthly_summary.items():
        print(f"  {category}: ${amount:.2f}")

def add_new_spending(manager):
    amount = float(input("Enter the amount spent: "))
    purchaser = input("Enter the purchaser's name: ")
    category = input("Enter the category: ")
    shop_name = input("Enter the shop name (optional): ")
    description = input("Enter the description (optional): ")
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