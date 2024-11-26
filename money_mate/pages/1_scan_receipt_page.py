import streamlit as st

from money_mate.utils.file_util import scan_uploaded_file

st.set_page_config(page_title="Scan Receipt")

st.title("Scan Receipt")

uploaded_file = st.file_uploader(
  "Choose a PNG, JPEG, or PDF file", type=["png", "jpeg", "jpg", "pdf"]
)

if uploaded_file is not None:
  try:
    receipt = scan_uploaded_file(uploaded_file)
  except ValueError:
    st.warning(f"{uploaded_file.name} is not supported, please upload a PNG, JPEG, or PDF file.")
  st.session_state.scanned_receipts.append(receipt)


st.subheader("Recently Scanned Receipts")
for receipt in st.session_state.scanned_receipts:
  st.text(f"📑 {receipt.filename} - Scanned at {receipt.timestamp}")