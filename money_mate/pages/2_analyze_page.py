import streamlit as st
import matplotlib.pyplot as plt
import logging
import os
import json
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger("money_mate.pages.2_analyze_page")

st.set_page_config(page_title="Analyze Finances")

st.title("Analyze Finances")

JSON_FILE = os.path.join(os.path.dirname(__file__), "scanned_receipts.json")

def load_receipts():
    """Load receipts from the local JSON file."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as file:
                receipts = json.load(file)
                logger.info(f"Loaded receipts: {receipts}")
                return receipts
        except json.JSONDecodeError:
            logger.warning("JSON file is empty or invalid. Starting with an empty list.")
            return []
    logger.info("No JSON file found. Starting with an empty list.")
    return []

# Aggregate data for the charts
def aggregate_spending_by_category(receipts):
    """Aggregate spending by category."""
    category_totals = defaultdict(float)
    for receipt in receipts:
        for item in receipt.get("items", []):
            category = item.get("category", "other")
            price = item.get("price", 0.0)
            category_totals[category] += price
    return category_totals

def aggregate_spending_by_company(receipts):
    """Aggregate spending by compnay."""
    company_totals = defaultdict(float)
    for receipt in receipts:
        for item in receipt.get("items", []):
            price = item.get("price", 0.0)
            company = receipt.get("company", "Unknown Company")
            company_totals[company] += price
    return company_totals

def aggregate_spending_by_date(receipts):
    """Aggregate total spending by date."""
    date_totals = defaultdict(float)
    for receipt in receipts:
        date = receipt.get("date", "Unknown Date")
        for item in receipt.get("items", []):
            price = item.get("price", 0.0)
            date_totals[date] += price
        # Debugging: Print each date's total after processing each receipt
        logger.info(f"Total for {date}: {date_totals[date]}")
    return date_totals


scanned_receipts = load_receipts()

category_totals = aggregate_spending_by_category(scanned_receipts)
company_totals = aggregate_spending_by_company(scanned_receipts)

# Display the charts
st.subheader("Spending by Category")

if category_totals:
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)
else:
    st.write("No data available to display the pie chart.")

st.subheader("Spending by Company")

if company_totals:
    labels = list(company_totals.keys())
    sizes = list(company_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)
else:
    st.write("No data available to display the pie chart.")

st.subheader("Total Spending Over Time")

date_totals = aggregate_spending_by_date(scanned_receipts)

if date_totals:
    sorted_dates = sorted(date_totals.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
    sorted_totals = [date_totals[date] for date in sorted_dates]

    fig, ax = plt.subplots()
    ax.plot(sorted_dates, sorted_totals, marker='o', linestyle='-', color='b')
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Amount Spent")
    ax.set_title("Total Spending Per Date")
    plt.xticks(rotation=45)

    st.pyplot(fig)
else:
    st.write("No data available to display the line chart.")