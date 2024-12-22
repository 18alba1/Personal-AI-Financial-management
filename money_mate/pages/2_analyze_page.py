import calendar
import logging
from datetime import datetime, date, timedelta

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import streamlit as st
import pandas as pd
import altair as alt

logger = logging.getLogger("money_mate.pages.2_analyze_page")

st.set_page_config(page_title="Analyze Finances")

st.title("Analyze Finances")

mpl.rcParams['font.size'] = 15


today = date.today()

col1, col2 = st.columns(2)

with col1:
    time_range = st.selectbox(
        "Quick Time Range",
        ["Daily", "Weekly", "Monthly", "Yearly"],
        index=2,  
        label_visibility="collapsed",
        placeholder="Quick Time Range"
    )

with col2:
    with st.expander("Custom Date Range"):
        custom_dates = st.checkbox("Use Custom Date Range", False)
        if custom_dates:
            custom_start = st.date_input(
                "Start Date", 
                value=date(today.year, today.month, 1),
                key="custom_start"
            )
            custom_end = st.date_input(
                "End Date", 
                value=today,
                key="custom_end"
            )

if custom_dates:
    start_date = custom_start
    end_date = custom_end
else:
    if time_range == "Daily":
        start_date = date.today()
        end_date = date.today()
    elif time_range == "Weekly":
        end_date = date.today()
        start_date = end_date - timedelta(days=end_date.weekday())
    elif time_range == "Monthly":
        start_date = date(today.year, today.month, 1)
        _, last_day = calendar.monthrange(today.year, today.month)
        end_date = date(today.year, today.month, last_day)
    else: 
        start_date = date(today.year, 1, 1)
        end_date = date(today.year, 12, 31)

st.caption(f"Showing data from {start_date} to {end_date}")

filtered_receipts = st.session_state.receipt_handler.filter_receipts_by_date(start_date, end_date)

# Debugging Info
logger.info(f"Start date: {start_date}")
logger.info(f"End date: {end_date}")

row1 = st.columns(2)
col1, col2 = row1

with col1:
  st.subheader("Spending by Category")

  category_totals = st.session_state.receipt_handler.aggregate_spending_by_category(
    start_date, end_date
  )

  if category_totals:
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=sns.color_palette("Set2"), startangle=90)
    plt.setp(texts, wrap=True)
    ax.axis("equal")

    st.pyplot(fig, use_container_width=True)
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

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
      sizes, labels=labels, autopct="%1.1f%%", colors=sns.color_palette("Set2_r"), 
      startangle=90, labeldistance=1.1 
    )
    ax.axis("equal")

    plt.setp(texts, wrap=True)

    hole = plt.Circle((0, 0), 0.65, facecolor="white")
    plt.gcf().gca().add_artist(hole)
    st.pyplot(fig, use_container_width=True)
  else:
    st.write("No data available to display the pie chart for companies.")


st.subheader("Total Spending Over Time")

date_totals = st.session_state.receipt_handler.aggregate_spending_by_date(start_date, end_date)

if date_totals:
  sorted_dates = sorted(date_totals.keys())
  sorted_totals = [date_totals[date] for date in sorted_dates]
  chart_data = pd.DataFrame({'Date':sorted_dates, 'Total Amount Spent':sorted_totals})
  points = alt.Chart(chart_data).mark_circle(
    size=60, 
    opacity=0.8
    ).encode(
    x='Date',
    y='Total Amount Spent',
    tooltip=['Date', 'Total Amount Spent']
  ).interactive()
  text = points.mark_text(
        align='center',
        baseline='bottom',
        color='#808080',
        dy=-7  
    ).encode(
        text=alt.Text('Total Amount Spent', format='.2f')  
    )
  line = alt.Chart(chart_data).mark_line().encode(
    x='Date',
    y='Total Amount Spent',
  ).interactive()
  chart = alt.layer(line, points, text).interactive()
  st.altair_chart(chart, use_container_width=True)
else:
  st.write("No data available to display the line chart.")

st.divider()  

st.subheader("Quick Stats")
col1, col2, col3 = st.columns(3)
if filtered_receipts:
    total_spent = sum(category_totals.values())
    num_transactions = len(filtered_receipts)
    avg_transaction = total_spent / num_transactions if num_transactions > 0 else 0
    with col1:
      st.metric("Total Spent", f"{total_spent:.2f}")
    with col2:  
      st.metric("Number of Transactions", num_transactions)
    with col3:
      st.metric("Average Transaction", f"{avg_transaction:.2f}")

st.subheader("💡 AI Financial Insights")
if st.button("Get Quick Insights"):
  if sorted_dates:
    earliest_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d").date()
    latest_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d").date()

    with st.spinner("Analyzing your spending patterns..."):
        try:
            insights = st.session_state.receipt_extraction_agent.get_simple_insights(
                st.session_state.receipt_handler,
                earliest_date,
                latest_date
            )
            st.markdown(insights)
        except Exception as e:
            st.error(f"Error generating insights: {str(e)}")
            logger.error(f"Error in insights generation: {e}", exc_info=True)
  else:
    st.write("no receipts during period.") 
