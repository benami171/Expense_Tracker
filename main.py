# main.py
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from SpendingManager import SpendingManager
from datetime import datetime

class SpendingManagerGUI:
    def __init__(self, master):
        self.master = master
        self.manager = SpendingManager()
        self.master.title("Spending Manager")
        self.master.geometry("500x370")  # Set a fixed size for the window
        self.master.configure(bg="#f0f0f0")  # Set a background color

        # Create a frame for the buttons
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(pady=10)

        # Buttons with modern styling
        self.view_button = ttk.Button(self.frame, text="View Current Month's Statistics", command=self.view_statistics)
        self.view_button.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(self.frame, text="Add New Spending", command=self.open_add_spending_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.frame, text="Remove Spending", command=self.remove_spending)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.master.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Add a title label
        self.title_label = ttk.Label(self.master, text="Spending Manager", font=("Helvetica", 16), background="#f0f0f0")
        self.title_label.pack(pady=10)

        # Text widget for displaying statistics
        self.stats_text = tk.Text(self.master, height=10, width=50, bg="#f0f0f0", font=("Helvetica", 12))
        self.stats_text.pack(pady=10)

    def open_add_spending_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Add New Spending")
        dialog.geometry("300x370")

        # Create labels and entry fields
        ttk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = ttk.Entry(dialog)
        amount_entry.pack(pady=5)

        ttk.Label(dialog, text="Purchaser's Name:").pack(pady=5)
        purchaser_entry = ttk.Entry(dialog)
        purchaser_entry.pack(pady=5)

        ttk.Label(dialog, text="Category:").pack(pady=5)
        category_combobox = ttk.Combobox(dialog, values=[
            "Housing", "Utilities", "Groceries", "Transportation", 
            "Healthcare", "Entertainment", "Personal Care", 
            "Clothing & Accessories", "Savings & Investments", 
            "Gifts", "Education", "Other"
        ])
        category_combobox.pack(pady=5)

        ttk.Label(dialog, text="Shop Name (optional):").pack(pady=5)
        shop_name_entry = ttk.Entry(dialog)
        shop_name_entry.pack(pady=5)

        ttk.Label(dialog, text="Description:").pack(pady=5)
        description_entry = ttk.Entry(dialog)
        description_entry.pack(pady=5)

        # Submit button
        submit_button = ttk.Button(dialog, text="Add Spending", command=lambda: self.add_spending(
            amount_entry.get(), purchaser_entry.get(), category_combobox.get(), 
            shop_name_entry.get(), description_entry.get(), dialog))
        submit_button.pack(pady=10)

    def add_spending(self, amount, purchaser, category, shop_name, description, dialog):
        try:
            amount = float(amount)
            if not all([purchaser, category, description]):
                raise ValueError("Please fill in all fields.")
            self.manager.add_spending(amount, purchaser, category, shop_name, description)
            self.view_statistics()  # Update statistics after adding spending
            dialog.destroy()  # Close the dialog
            messagebox.showinfo("Success", "Spending added successfully!")
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))

    def view_statistics(self):
        current_date = datetime.now()
        monthly_summary = self.manager.get_monthly_summary(current_date.year, current_date.month)
        total_spent = sum(monthly_summary.values())
        average_spending = total_spent / current_date.day if current_date.day > 0 else 0
        previous_average = self.manager.get_average_spending(current_date.year, current_date.month)

        # Clear the text widget
        self.stats_text.delete(1.0, tk.END)

        # Insert the statistics into the text widget
        stats = f"Total spent this month: ₪{total_spent:.2f}\n"
        stats += f"Average spending per day: ₪{average_spending:.2f}\n"
        stats += f"Average spending of previous months: ₪{previous_average:.2f}\n"
        
        self.stats_text.insert(tk.END, stats)

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
            self.view_statistics()  # Update statistics after removing spending
            messagebox.showinfo("Removed Spending", f"Removed spending: ₪{removed_spending.amount:.2f} - {removed_spending.category} - {removed_spending.description}")
        else:
            messagebox.showwarning("Invalid Choice", "Please select a valid spending number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpendingManagerGUI(root)
    root.mainloop()