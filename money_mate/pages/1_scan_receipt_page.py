import logging
import json
import os
import streamlit as st
from money_mate.utils.file_util import get_image_base64
from money_mate.types.receipt_type import Receipt

logger = logging.getLogger("money_mate.pages.1_scan_receipt_page")

st.set_page_config(page_title="Scan Receipt")

st.title("Scan Receipt")

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

def save_receipts(receipts):
    """Save receipts to the local JSON file."""
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(receipts, file, indent=4)
        logger.info(f"Receipts successfully saved: {receipts}")
    except Exception as e:
        logger.error(f"Error saving receipts: {e}")

# Load existing receipts
scanned_receipts = load_receipts()

uploaded_file = st.file_uploader("Choose a PNG, JPG, or JPEG file", type=["png", "jpeg", "jpg"])

if uploaded_file is not None:
    with st.spinner("Parsing the image"):
        
        image_base64 = get_image_base64(uploaded_file)
        
        # Extract receipt data
        receipt = st.session_state.receipt_extraction_agent.scan_image_bytes(image_base64)
        
        if isinstance(receipt, Receipt):
            receipt = receipt.model_dump()

        scanned_receipts.append(receipt)
        logger.info(f"Appended receipt: {receipt}")

        save_receipts(scanned_receipts)
        
        logger.info(f"scanned_receipts now contains {len(scanned_receipts)} receipts")
        st.success("Receipt saved successfully!")
