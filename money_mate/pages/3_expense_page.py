import os
import json
import pandas as pd
import streamlit as st

JSON_FILE = os.path.join(os.path.dirname(__file__), "scanned_receipts.json")

def load_receipts():
    """Load receipts from the local JSON file."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.warning("Receipts file is empty or corrupted.")
            return []
    st.warning("No receipts file found.")
    return []

def prepare_table_data(receipts):
    """Flatten receipts data into a table-friendly format."""
    table_data = []
    for receipt in receipts:
        for item in receipt["items"]:
            table_data.append({
                "Company": receipt["company"],
                "Date": receipt["date"],
                "Item Name": item["name"],
                "Price": item["price"],
                "Category": item["category"],
            })
    return table_data

# Load receipts
receipts = load_receipts()

# Prepare data for the table
if receipts:
    table_data = prepare_table_data(receipts)

    # Convert to DataFrame for display
    df = pd.DataFrame(table_data)

    # Display the DataFrame as a table
    st.title("Expense History")
    st.write("Below is the table of all your scanned receipts:")
    st.dataframe(df)
else:
    st.warning("No receipt history to display.")
