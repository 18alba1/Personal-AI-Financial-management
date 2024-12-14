import logging

import streamlit as st

from money_mate.agents.receipt_extraction_agent import ReceiptExtractionAgent

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

if "scanned_receipts" not in st.session_state:
    st.session_state.scanned_receipts = []

if "receipt_extraction_agent" not in st.session_state:
    st.session_state.receipt_extraction_agent = ReceiptExtractionAgent(
        st.secrets["openai_model"], st.secrets["openai_key"]
    )

st.title("Welcome to MoneyMate! 💰")

st.write(
    """
    **MoneyMate** is your personal finance management system powered by AI to help you stay on top of your spending effortlessly.
    With MoneyMate, you can easily analyze your expenses and receive personalized financial insights.
    """
)

st.header("How It Works")

st.write(
    """
    1. **Scan Your Receipts**:
       - Go to the **Scan Receipt** page and upload your receipts as images.
       - Our AI-powered image recognition will automatically extract key details such as:
         - Purchase amounts
         - Item names and categories (e.g., food, travel, shopping)

    2. **View Your Purchase History**:
       - Head to the **Expense** page to see a complete list of your scanned receipts.
       - Track where your money is going and review your spending habits.

    3. **Analyze Your Finances**:
       - On the **Analyze** page, gain valuable insights with visualizations:
         - **Spending by Category**: Discover which categories (e.g., food, travel) you spend the most on.
         - **Spending by Company**: See which companies you frequently purchase from.
         - **Time-Based Analysis**: Filter your spending by day, week, month, year, or a custom date range.

    4. **AI-Powered Financial Advice**:
       - Get personalized suggestions on how to improve your finances based on your spending data.

    ### Get Started!
    Simply upload your receipts on the **Scan Receipt** page, and let MoneyMate do the rest.  
    Manage your money smarter, visualize your spending, and improve your financial health with AI insights!
    """
)
