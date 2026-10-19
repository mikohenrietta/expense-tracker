import streamlit as st
from services.Service import ExpenseService

st.set_page_config(page_title="Regional Expense Tracker", layout="wide")


# Initialize Service
@st.cache_resource
def get_service():
    return ExpenseService()


service = get_service()

st.title("Regional Expense Tracker")

# --- CREATE OPERATION ---
with st.sidebar.form("add_expense_form", clear_on_submit=True):
    st.header("Add New Record")
    date_input = st.date_input("Date")
    expenses_input = st.text_input("Expense Description")
    category_input = st.selectbox("Category", ["Housing", "Transport", "Food", "Utilities", "Other"])
    amount_input = st.number_input("Amount", min_value=0.0, format="%.2f")
    municipality_input = st.text_input("Municipality")
    province_input = st.text_input("Province")
    region_input = st.text_input("Region")

    submit = st.form_submit_button("Save")
    if submit:
        service.add_expense(
            date_input, expenses_input, category_input, amount_input,
            municipality_input, province_input, region_input
        )
        st.success("Record added successfully!")
        st.rerun()

# --- READ OPERATION ---
df = service.get_expenses_df()

if not df.empty:
    st.subheader("Expense Records")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No data available. Add a record or load your Kaggle dataset.")

# --- DELETE OPERATION ---
st.subheader("Delete Record")
with st.form("delete_form"):
    del_id = st.number_input("Enter ID to delete", min_value=1, step=1)
    del_submit = st.form_submit_button("Delete")
    if del_submit:
        success = service.delete_expense(del_id)
        if success:
            st.success(f"Record {del_id} deleted.")
            st.rerun()
        else:
            st.error("ID not found.")