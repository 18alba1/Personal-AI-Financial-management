import streamlit as st

st.set_page_config(
  page_title="Welcome to MoneyMate!",
  page_icon="💰",
)

# Initialization
if "scanned_receipts" not in st.session_state:
  st.session_state.scanned_receipts = []
