import pandas as pd
import streamlit as st


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Draw the sidebar filters and return only the rows that match them."""
    if df.empty:
        return df

    with st.sidebar:
        st.header("Filters")

        date_range = st.date_input(
            "Date range",
            value=(df["Date"].min(), df["Date"].max()),
        )

        all_categories = sorted(df["Category"].unique())
        categories = st.multiselect("Category", all_categories, default=all_categories)

        search = st.text_input("Search expense", placeholder="e.g. rent")

    filtered = df[df["Category"].isin(categories)]

    # While the user is still picking the end date, date_input returns only one date
    if len(date_range) == 2:
        start, end = date_range
        filtered = filtered[(filtered["Date"] >= start) & (filtered["Date"] <= end)]

    if search:
        filtered = filtered[
            filtered["Expenses"].str.contains(search, case=False, regex=False, na=False)
        ]

    return filtered