import streamlit as st

st.title("Expense History")
st.write("Below is the table of all your scanned receipts:")

df = st.session_state.receipt_handler.to_pandas_dataframe()

if not df.empty:
  st.dataframe(df)
else:
  st.warning("No receipt history to display.")


# st.write(st.session_state.receipt_handler.to_string())
