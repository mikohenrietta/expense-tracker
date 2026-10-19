import pandas as pd
from datetime import datetime
from repositories.Repository import ExpenseRepository
from models.Expense import Expense


class ExpenseService:
    def __init__(self):
        self.repo = ExpenseRepository()

    def add_expense(self, date_str, expenses, category, amount):
        # Business logic: Convert string to date object
        parsed_date = datetime.strptime(str(date_str), "%Y-%m-%d").date()

        new_expense = Expense(
            date=parsed_date,
            expenses=expenses,
            category=category,
            amount=amount
        )
        return self.repo.add(new_expense)

    def get_expenses_df(self):
        # Convert SQLAlchemy objects to Pandas DataFrame for Streamlit
        records = self.repo.get_all()
        data = [{
            "ID": r.id,
            "Date": r.date,
            "Expenses": r.expenses,
            "Category": r.category,
            "Amount": r.amount
        } for r in records]
        return pd.DataFrame(data)

    def update_expense(self, expense_id, date_str, expenses, category, amount):
        parsed_date = datetime.strptime(str(date_str), "%Y-%m-%d").date()
        return self.repo.update(
            expense_id,
            date=parsed_date,
            expenses=expenses,
            category=category,
            amount=amount
        )

    def delete_expense(self, expense_id):
        return self.repo.delete(expense_id)
