import os
import sys
import base64
import streamlit as st
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from MoneyMate import util
from MoneyMate.imageHandler import create_analyzer

'''
def view():
  st.title("Scan Receipt")


  uploaded_file = st.file_uploader("Choose a PNG, JPEG, or PDF file", type=["png", "jpeg", "jpg", "pdf"])
  if uploaded_file is not None:
    st.write("filename:", uploaded_file.name)
    #st.write(base64.b64encode(uploaded_file.getvalue()).decode('utf-8'))
    st.write(util.convert_bytes_to_text(base64.b64encode(uploaded_file.getvalue())))
'''

def view():
    st.title("Scan Receipt")

    # Initialize session state for storing extracted text if not exists
    if 'scanned_receipts' not in st.session_state:
        st.session_state.scanned_receipts = []

    uploaded_file = st.file_uploader("Choose a PNG, JPEG, or PDF file", type=["png", "jpeg", "jpg", "pdf"])
    if uploaded_file is not None:
        st.write("filename:", uploaded_file.name)
        
        # Display the uploaded file
        file_bytes = uploaded_file.getvalue()
        file_type = uploaded_file.type
        
        if file_type.startswith('image'):
            st.image(file_bytes, caption='Uploaded Image', use_column_width=True)

            try:
                # Extract text
                extracted_text = util.convert_bytes_to_text(base64.b64encode(file_bytes))
                
                # Create a receipt entry
                receipt_entry = {
                    'filename': uploaded_file.name,
                    'text': extracted_text,
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                if not any(r['filename'] == uploaded_file.name for r in st.session_state.scanned_receipts):
                        st.session_state.scanned_receipts.append(receipt_entry)
                        st.success("Receipt scanned successfully! Go to the Analyze page to see the analysis.")
                else:
                    st.info("This receipt has already been scanned.")
                
                # Show extracted text in an expander
                with st.expander("View Extracted Text"):
                    st.text(extracted_text)

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

        else:
          st.error("Please upload an image file (PNG, JPEG, or JPG)")
    else:
        # Show instructions when no file is uploaded
        st.info("📱 Take a photo of your receipt or upload an existing one to get started")
        st.markdown("""
        Supported file types:
        - Images (PNG, JPEG, JPG)
        """)

     # Show list of scanned receipts
    if st.session_state.scanned_receipts:
        st.subheader("Recently Scanned Receipts")
        for receipt in st.session_state.scanned_receipts:
            st.text(f"📑 {receipt['filename']} - Scanned at {receipt['timestamp']}")