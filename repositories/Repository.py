from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.Expense import Base, Expense


DB_PATH = Path(__file__).resolve().parent.parent / "expenses.db"
DEFAULT_DB_URL = f"sqlite:///{DB_PATH}"

class ExpenseRepository:
    def __init__(self, db_url=DEFAULT_DB_URL):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add(self, expense: Expense):
        with self.Session() as session:
            session.add(expense)
            session.commit()
            session.refresh(expense)
            return expense

    def get_all(self):
        with self.Session() as session:
            return session.query(Expense).order_by(Expense.date.desc(), Expense.id.desc()).all()

    def update(self, expense_id: int, **fields):
        with self.Session() as session:
            expense = session.query(Expense).filter_by(id=expense_id).first()
            if expense:
                for name, value in fields.items():
                    setattr(expense, name, value)
                session.commit()
                return True
            return False

    def delete(self, expense_id: int):
        with self.Session() as session:
            expense = session.query(Expense).filter_by(id=expense_id).first()
            if expense:
                session.delete(expense)
                session.commit()
                return True
            return False
