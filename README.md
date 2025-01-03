# Personal-AI-Financial-management
This project:MoneyMate is a personal finance management system powered by AI to help you analyze your expenses by scanning your receipts and receiving personalized financial insights according to them.

## How the website works
1. Scan Your Receipts on the Scan Receipt page.
2. View Your Purchase History on the Expense page.
3. On the Analyze page, gain valuable insights with visualizations.
4. Get AI-Powered Financial Advice based on your spending data.

## How to run the project

First you need to install all the dependecies:
```
pip install -e .
```

Then, modify the `.streamlit/example_secrets.toml` file to include the OpenAI key and rename it to `.streamlit/secrets.toml`

Now, you can run the streamlit application by:
```
streamlit run money_mate/home_page.py
```
