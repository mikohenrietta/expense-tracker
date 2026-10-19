import streamlit as st
from services.Service import ExpenseService

st.set_page_config(page_title="Expense tracker", layout="wide")

CATEGORIES = ["Survival", "Optional", "Obligation", "Unexpected"]


# Initialize Service
@st.cache_resource
def get_service():
    return ExpenseService()


service = get_service()

# Used to reset the table selection after a record changes
if "table_version" not in st.session_state:
    st.session_state.table_version = 0


def finish(message):
    st.session_state.toast = message
    st.session_state.table_version += 1
    st.rerun()


if "toast" in st.session_state:
    st.toast(st.session_state.pop("toast"), icon=":material/check_circle:")

st.title("Expense tracker")

df = service.get_expenses_df()
expense_types = sorted(df["Expenses"].unique()) if not df.empty else []


def expense_form(form_key, record=None):
    """Shared inputs for adding and editing. Returns the submitted values or None."""
    with st.form(form_key, clear_on_submit=record is None, border=record is not None):
        date_input = st.date_input("Date", value=record["Date"] if record is not None else "today")
        expenses_input = st.selectbox(
            "Expense",
            expense_types,
            index=expense_types.index(record["Expenses"]) if record is not None and record["Expenses"] in expense_types else None,
            placeholder="Choose or type a new one",
            accept_new_options=True,
        )
        category_input = st.segmented_control(
            "Category",
            CATEGORIES,
            default=record["Category"] if record is not None else CATEGORIES[0],
        )
        amount_input = st.number_input(
            "Amount",
            min_value=0.0,
            value=float(record["Amount"]) if record is not None else 0.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("Save", type="primary", icon=":material/save:", width="stretch")

    if not submitted:
        return None
    if not expenses_input or not category_input or amount_input <= 0:
        st.error("Please fill in the expense, category and an amount greater than 0.")
        return None
    return date_input, expenses_input, category_input, amount_input


# --- CREATE OPERATION ---
with st.sidebar:
    st.header("Add expense")
    values = expense_form("add_expense_form")
    if values:
        service.add_expense(*values)
        finish("Expense added.")


# --- UPDATE OPERATION ---
@st.dialog("Edit expense")
def edit_dialog(record):
    values = expense_form("edit_expense_form", record)
    if values:
        service.update_expense(int(record["ID"]), *values)
        finish("Expense updated.")


# --- DELETE OPERATION ---
@st.dialog("Delete expense")
def delete_dialog(record):
    st.write(f"Delete **{record['Expenses']}** ({record['Amount']:.2f}) from {record['Date']}?")
    st.caption("This can't be undone.")
    with st.container(horizontal=True, horizontal_alignment="right"):
        if st.button("Cancel"):
            st.rerun()
        if st.button("Delete", type="primary", icon=":material/delete:"):
            service.delete_expense(int(record["ID"]))
            finish("Expense deleted.")


# --- READ OPERATION ---
if df.empty:
    st.info("No expenses yet. Add one from the sidebar.")
    st.stop()

with st.container(horizontal=True, vertical_alignment="bottom"):
    st.subheader("Expenses")
    st.caption("Select a row to edit or delete it.")

event = st.dataframe(
    df,
    hide_index=True,
    column_order=["Date", "Expenses", "Category", "Amount"],
    column_config={
        "Date": st.column_config.DateColumn("Date", format="MMM D, YYYY"),
        "Expenses": "Expense",
        "Amount": st.column_config.NumberColumn("Amount", format="%.2f"),
    },
    on_select="rerun",
    selection_mode="single-row",
    key=f"expense_table_{st.session_state.table_version}",
    alt="Table of expenses",
)

selected_rows = event.selection.rows
selected = df.iloc[selected_rows[0]] if selected_rows else None

with st.container(horizontal=True):
    if st.button("Edit", icon=":material/edit:", disabled=selected is None):
        edit_dialog(selected)
    if st.button("Delete", icon=":material/delete:", disabled=selected is None):
        delete_dialog(selected)
