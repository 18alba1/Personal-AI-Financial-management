import os
import sys
# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from MoneyMate.views import scanReceipt
from MoneyMate import util

import analyze
import expense
import scanReceipt
import streamlit as st



def homepage_view():
  st.title("Welcome to MoneyMate!")

  st.markdown("""
    * Use the menu at left to select services
    * 
    """)


# Sidebar navigation
st.sidebar.title("Services")
page = st.sidebar.radio(
  "Go to", ("Homepage", "Scan Receipt", "Expense Manager", "Analyze Finances")
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
