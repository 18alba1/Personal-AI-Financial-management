import logging

import streamlit as st

from money_mate.utils.file_util import get_image_base64

logger = logging.getLogger("money_mate.pages.1_scan_receipt_page")

st.set_page_config(page_title="Scan Receipt")

st.title("Scan Receipt")

uploaded_file = st.file_uploader("Choose a PNG, JPG, or JPEG file", type=["png", "jpeg", "jpg"])

if uploaded_file is not None:
  with st.spinner("Parsing the image"):
    image_base64 = get_image_base64(uploaded_file)

    # Extract receipt data
    receipt = st.session_state.receipt_extraction_agent.scan_image_bytes(image_base64)

    # Save the new receipt
    st.session_state.receipt_handler.save_new_receipt(receipt)

    st.success("Receipt saved successfully!")
