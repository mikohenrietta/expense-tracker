import pandas as pd
import streamlit as st


def render_summary(df: pd.DataFrame):
    """Totals shown above the table."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Total spent", f"{df['Amount'].sum():,.2f}")
    col2.metric("Average expense", f"{df['Amount'].mean():,.2f}")
    col3.metric("Number of expenses", f"{len(df):,}")


def render_charts(df: pd.DataFrame):
    """Spending per month and per category."""
    month = pd.to_datetime(df["Date"]).dt.to_period("M").dt.to_timestamp()
    per_month = df.groupby(month)["Amount"].sum()
    per_category = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    left, right = st.columns(2)
    with left:
        st.subheader("Spending per month")
        st.line_chart(per_month)
    with right:
        st.subheader("Spending per category")
        st.bar_chart(per_category)