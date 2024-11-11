# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Import ttk for themed widgets
from SpendingManager import SpendingManager
from datetime import datetime

class SpendingManagerGUI:
    def __init__(self, master):
        self.master = master
        self.manager = SpendingManager()
        self.master.title("Spending Manager")
        self.master.geometry("400x300")  # Set a fixed size for the window
        self.master.configure(bg="#f0f0f0")  # Set a background color

        # Create a frame for the buttons
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(pady=10)

        # Buttons with modern styling
        self.view_button = ttk.Button(self.frame, text="View Current Month's Statistics", command=self.view_statistics)
        self.view_button.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(self.frame, text="Add New Spending", command=self.add_spending)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.frame, text="Remove Spending", command=self.remove_spending)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.master.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Add a title label
        self.title_label = ttk.Label(self.master, text="Spending Manager", font=("Helvetica", 16), background="#f0f0f0")
        self.title_label.pack(pady=10)

    def view_statistics(self):
        current_date = datetime.now()
        monthly_summary = self.manager.get_monthly_summary(current_date.year, current_date.month)
        total_spent = sum(monthly_summary.values())
        average_spending = total_spent / current_date.day if current_date.day > 0 else 0
        previous_average = self.manager.get_average_spending(current_date.year, current_date.month)

        stats = f"Total spent this month: ₪{total_spent:.2f}\n"
        stats += f"Average spending per day: ₪{average_spending:.2f}\n"
        stats += f"Average spending of previous months: ₪{previous_average:.2f}\n"
        
        messagebox.showinfo("Current Month's Spending Statistics", stats)

    def add_spending(self):
        amount = simpledialog.askfloat("Input", "Enter the amount spent:")
        purchaser = simpledialog.askstring("Input", "Enter the purchaser's name:")
        category = simpledialog.askstring("Input", "Enter the category:")
        shop_name = simpledialog.askstring("Input", "Enter the shop name (optional):")
        description = simpledialog.askstring("Input", "What did you buy? (description):")
        
        if amount and purchaser and category and description:
            self.manager.add_spending(amount, purchaser, category, shop_name, description)
            messagebox.showinfo("Success", "Spending added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def remove_spending(self):
        spendings = self.manager.spendings
        if not spendings:
            messagebox.showwarning("No Spendings", "There are no spendings to remove.")
            return
        
        spending_list = "\n".join([f"{i + 1}. ₪{s.amount:.2f} - {s.category} - {s.description}" for i, s in enumerate(spendings)])
        choice = simpledialog.askinteger("Remove Spending", f"Select a spending to remove:\n{spending_list}\nEnter the number:")
        
        if choice and 1 <= choice <= len(spendings):
            removed_spending = spendings.pop(choice - 1)
            self.manager.save_spendings()
            messagebox.showinfo("Removed Spending", f"Removed spending: ₪{removed_spending.amount:.2f} - {removed_spending.category} - {removed_spending.description}")
        else:
            messagebox.showwarning("Invalid Choice", "Please select a valid spending number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpendingManagerGUI(root)
    root.mainloop()