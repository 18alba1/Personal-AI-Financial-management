import streamlit as st
import matplotlib.pyplot as plt
import logging
import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

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

def filter_receipts_by_date(receipts, start_date, end_date):
    """Filter receipts within a given date range."""
    filtered = [
        receipt for receipt in receipts
        if start_date <= datetime.strptime(receipt["date"], "%Y-%m-%d") <= end_date
    ]
    return filtered

scanned_receipts = load_receipts()

st.sidebar.title("Filter Options")

# Default date range
default_start_date = datetime.today() - timedelta(days=30)
default_end_date = datetime.today()

start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)

# Convert to datetime objects
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.max.time())

st.sidebar.write("Quick Filter Options:")

if st.sidebar.button("Daily"):
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999)

if st.sidebar.button("Weekly"):
    end_date = datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = end_date - timedelta(days=7)

if st.sidebar.button("Monthly"):
    today = datetime.today()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        end_date = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    else:
        first_day_next_month = today.replace(month=today.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = first_day_next_month - timedelta(seconds=1)

if st.sidebar.button("Yearly"):
    today = datetime.today()
    start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

# Filter receipts by date range
filtered_receipts = filter_receipts_by_date(scanned_receipts, start_date, end_date)

# Debugging Info
st.sidebar.write(f"Start Date: {start_date}")
st.sidebar.write(f"End Date: {end_date}")


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
    """Aggregate spending by company."""
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
    return date_totals


st.subheader("Spending by Category")

category_totals = aggregate_spending_by_category(filtered_receipts)

if category_totals:
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)
else:
    st.write("No data available to display the pie chart for categories.")


st.subheader("Spending by Company")

company_totals = aggregate_spending_by_company(filtered_receipts)

if company_totals:
    labels = list(company_totals.keys())
    sizes = list(company_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)
else:
    st.write("No data available to display the pie chart for companies.")


st.subheader("Total Spending Over Time")

date_totals = aggregate_spending_by_date(filtered_receipts)

if date_totals:
    sorted_dates = sorted(date_totals.keys())
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
