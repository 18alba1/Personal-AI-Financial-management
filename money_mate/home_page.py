import logging
import streamlit as st

from money_mate.agents.receipt_extraction_agent import ReceiptExtractionAgent


# Create a logger for application's namespace
logger = logging.getLogger("money_mate")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


st.set_page_config(
  page_title="Welcome to MoneyMate!",
  page_icon="💰",
)

# Initialization
if "scanned_receipts" not in st.session_state:
  st.session_state.scanned_receipts = []

if "receipt_extraction_agent" not in st.session_state:
  st.session_state.receipt_extraction_agent = ReceiptExtractionAgent(
    st.secrets["openai_model"], st.secrets["openai_key"])