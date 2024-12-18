import calendar
import logging
from datetime import date, timedelta

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

logger = logging.getLogger("money_mate.pages.2_analyze_page")

st.set_page_config(page_title="Analyze Finances")

st.title("Analyze Finances")

row1 = st.columns(2)
col1, col2 = row1

st.sidebar.title("Filter Options")


today = date.today()
# Get the first day of the current month
default_start_date = date(today.year, today.month, 1)
# Get the last day of the current month
_, last_day = calendar.monthrange(today.year, today.month)
default_end_date = date(today.year, today.month, last_day)

start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)

st.sidebar.write("Quick Filter Options:")

if st.sidebar.button("Daily"):
  start_date = date.today()
  end_date = date.today()

if st.sidebar.button("Weekly"):
  end_date = date.today()
  # Calculate the start of the current week (Monday)
  start_date = end_date - timedelta(days=end_date.weekday())

if st.sidebar.button("Monthly"):
  # First day of current month
  start_date = date(today.year, today.month, 1)
  # Last day of current month
  _, last_day = calendar.monthrange(today.year, today.month)
  end_date = date(today.year, today.month, last_day)

if st.sidebar.button("Yearly"):
  # First day of current year
  start_date = date(today.year, 1, 1)
  # Last day of current year
  end_date = date(today.year, 12, 31)

# Filter receipts by date range
filtered_receipts = st.session_state.receipt_handler.filter_receipts_by_date(start_date, end_date)

# Debugging Info
logger.info(f"Start date: {start_date}")
logger.info(f"End date: {end_date}")


with col1:
  st.subheader("Spending by Category")

  category_totals = st.session_state.receipt_handler.aggregate_spending_by_category(
    start_date, end_date
  )

  if category_totals:
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=sns.color_palette("Set2"), startangle=90)
    ax.axis("equal")

    st.pyplot(fig)
  else:
    st.write("No data available to display the pie chart for categories.")

with col2:
  st.subheader("Spending by Company")

  company_totals = st.session_state.receipt_handler.aggregate_spending_by_company(
    start_date, end_date
  )

  if company_totals:
    labels = list(company_totals.keys())
    sizes = list(company_totals.values())

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
      sizes, labels=labels, autopct="%1.1f%%", colors=sns.color_palette("Paired"), startangle=90
    )
    ax.axis("equal")

    hole = plt.Circle((0, 0), 0.65, facecolor="white")
    plt.gcf().gca().add_artist(hole)
    st.pyplot(fig)
  else:
    st.write("No data available to display the pie chart for companies.")


st.subheader("Total Spending Over Time")

date_totals = st.session_state.receipt_handler.aggregate_spending_by_date(start_date, end_date)

if date_totals:
  sorted_dates = sorted(date_totals.keys())
  sorted_totals = [date_totals[date] for date in sorted_dates]

  fig, ax = plt.subplots(figsize=(10, 5))
  ax.plot(sorted_dates, sorted_totals, marker="o", linestyle="-", color="#EDB120")
  ax.set_xlabel("Date")
  ax.set_ylabel("Total Amount Spent")
  ax.set_title("Total Spending Per Date")
  plt.xticks(rotation=45)

  st.pyplot(fig)
else:
  st.write("No data available to display the line chart.")