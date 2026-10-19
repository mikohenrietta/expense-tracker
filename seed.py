import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from models.Expense import Base

# 1. Set up the SQLite database connection
# This will create 'expenses.db' in your folder if it doesn't exist
engine = create_engine("sqlite:///expenses.db")

# Create the tables based on your model.py
Base.metadata.create_all(engine)

# 2. Read the Excel file
print("Loading data from Excel...")
current_dir = Path(__file__).parent
file_path = current_dir / "data" / "expenses_data.xlsx"

df = pd.read_excel(file_path, engine="openpyxl")

# 3. Map the Excel column names to your SQLAlchemy model's column names
# (Pandas is case-sensitive, so we map the capitalized Excel headers to lowercase)
# Map the Excel column names
df = df.rename(columns={
    "Date": "date",
    "Expenses": "expenses",
    "Category": "category",
    "Amount": "amount",
    "Municipality": "municipality",
    "Province": "province",
    "Region": "region"
})

if "ID" in df.columns:
    df = df.drop(columns=["ID"])

df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

# Push the data into the 'expenses' table
print("Writing data to SQLite...")
df.to_sql("expenses", con=engine, if_exists="append", index=False)

print("Database seeded successfully!")