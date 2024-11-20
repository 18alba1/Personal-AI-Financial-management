import streamlit as st
import scanReceipt
import expense
import analyze

def homepage_view():
    st.title('Welcome to MoneyMate!')

    st.markdown("""
    * Use the menu at left to select services
    * 
    """)

# Sidebar navigation
st.sidebar.title("Services")
page = st.sidebar.radio(
    "Go to",
    ("Homepage", "Scan Receipt", "Expense Manager", "Analyze Finances")
)

# Routing logic
if page == "Homepage":
    homepage_view()
elif page == "Scan Receipt":
    scanReceipt.view()
elif page == "Expense Manager":
    expense.view()
elif page == "Analyze Finances":
    analyze.view()
