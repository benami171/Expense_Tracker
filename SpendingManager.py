import json
from datetime import datetime
from collections import defaultdict

class Spending:
    def __init__(self, date, amount, purchaser, category, shop_name="", description=""):
        self.date = date
        self.amount = amount
        self.purchaser = purchaser
        self.category = category
        self.shop_name = shop_name
        self.description = description
        
    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "amount": self.amount,
            "purchaser": self.purchaser,
            "category": self.category,
            "shop_name": self.shop_name,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        date = datetime.fromisoformat(data["date"])
        return Spending(date, data["amount"], data["purchaser"], data["category"], data["shop_name"], data["description"])

class SpendingManager:
    def __init__(self, filename='spendings.json'):
        self.spendings = []
        self.filename = filename
        self.load_spendings()

    def add_spending(self, amount, purchaser, category, shop_name="", description=""):
        date = datetime.now()
        spending = Spending(date, amount, purchaser, category, shop_name, description)
        self.spendings.append(spending)
        self.save_spendings()  # Save after adding a new spending

    def save_spendings(self):
        with open(self.filename, 'w') as f:
            json.dump([spending.to_dict() for spending in self.spendings], f)

    def load_spendings(self):
        try:
            with open(self.filename, 'r') as f:
                spendings_data = json.load(f)
                self.spendings = [Spending.from_dict(data) for data in spendings_data]
        except FileNotFoundError:
            self.spendings = []  # If the file doesn't exist, start with an empty list

    def get_monthly_summary(self, year, month):
        monthly_spendings = defaultdict(float)
        for spending in self.spendings:
            if spending.date.year == year and spending.date.month == month:
                monthly_spendings[spending.category] += spending.amount
        return dict(monthly_spendings)

    def get_purchaser_summary(self, year, month, purchaser):
        total = 0
        for spending in self.spendings:
            if (spending.date.year == year and 
                spending.date.month == month and 
                spending.purchaser == purchaser):
                total += spending.amount
        return total

    def get_category_breakdown(self, year, month):
        categories = defaultdict(lambda: defaultdict(float))
        for spending in self.spendings:
            if spending.date.year == year and spending.date.month == month:
                categories[spending.category][spending.purchaser] += spending.amount
        return dict(categories)


