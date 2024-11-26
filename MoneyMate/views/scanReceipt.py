import streamlit as st
import base64

def view():
  st.title("Scan Receipt")

  uploaded_file = st.file_uploader("Choose a PNG, JPEG, or PDF file", type=["png", "jpeg", "jpg", "pdf"])
  if uploaded_file is not None:
    st.write("filename:", uploaded_file.name)
    st.write(base64.b64encode(uploaded_file.getvalue()).decode('utf-8'))
