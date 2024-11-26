import base64

from streamlit.runtime.uploaded_file_manager import UploadedFile

from money_mate.types.receipt_type import Receipt


def get_image_base64(uploaded_file: UploadedFile) -> Receipt:
  file_bytes = uploaded_file.getvalue()
  return base64.b64encode(file_bytes).decode("utf-8")
