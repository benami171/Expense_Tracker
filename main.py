# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from SpendingManager import SpendingManager
from datetime import datetime

def display_menu():
    print("\n--- Spending Manager ---")
    print("1. View current month's spending statistics")
    print("2. Add a new spending")
    print("3. Remove a spending")
    print("4. Exit")

def get_current_month_statistics(manager):
    current_date = datetime.now()
    monthly_summary = manager.get_monthly_summary(current_date.year, current_date.month)
    
    # Calculate total spent and average spending
    total_spent = sum(monthly_summary.values())
    average_spending = total_spent / current_date.day if current_date.day > 0 else 0
    previous_average = manager.get_average_spending(current_date.year, current_date.month)

    print("\n--- Current Month's Spending Statistics ---")
    print(f"Total spent this month: ₪{total_spent:.2f}")
    print(f"Average spending per day: ₪{average_spending:.2f}")
    print(f"Average spending of previous months: ₪{previous_average:.2f}")
    
    print("\nSpending details:")
    print(f"{'Amount (₪)':<15} {'Category':<30} {'Description':<40}")  # Table header
    print("-" * 85)  # Separator

    # Display each spending entry
    for spending in manager.spendings:
        if spending.date.year == current_date.year and spending.date.month == current_date.month:
            print(f"₪{spending.amount:<15.2f} {spending.category:<30} {spending.description:<40}")

    print("-" * 85)  # Separator

    # Comparison message moved to the bottom
    if total_spent < previous_average:
        print("💸💸 Great job! You're spending less than your average. Keep it up!💸💸")
    elif total_spent > previous_average:
        print("😰😱Uh-oh! Looks like you spending more than usual did you won the lottery? 😅")
    else:
        print("Your spending is exactly at your average. Balance is key!")

    print()  # Add an empty line for better readability

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

def remove_spending(manager):
    print("\n--- Current Spendings ---")
    for index, spending in enumerate(manager.spendings):
        print(f"{index + 1}. ₪{spending.amount:.2f} - {spending.category} - {spending.description} (Date: {spending.date})")

    try:
        choice = int(input("Enter the number of the spending you want to remove: "))
        if 1 <= choice <= len(manager.spendings):
            removed_spending = manager.spendings.pop(choice - 1)  # Remove the spending
            manager.save_spendings()  # Save the updated list
            print(f"Removed spending: ₪{removed_spending.amount:.2f} - {removed_spending.category} - {removed_spending.description}")
        else:
            print("Invalid choice. No spending removed.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    manager = SpendingManager()

    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            get_current_month_statistics(manager)
        elif choice == '2':
            add_new_spending(manager)
        elif choice == '3':
            remove_spending(manager)  # Call the new remove function
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()