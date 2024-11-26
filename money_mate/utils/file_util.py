import io
from datetime import datetime
from pathlib import Path

import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from streamlit.runtime.uploaded_file_manager import UploadedFile

from money_mate.types.file_type import FileType
from money_mate.types.receipt_type import Receipt


def scan_uploaded_file(uploaded_file: UploadedFile) -> Receipt:
  file_bytes = uploaded_file.getvalue()
  file_type = FileType.from_filename(Path(uploaded_file.name))

  if file_type == FileType.OTHER:
    raise ValueError(f"{uploaded_file.name} not supported")

  read_text = ""
  if file_type in (FileType.JPG, FileType.PNG):
    read_text = scan_image_file(file_bytes)
  elif file_type == FileType.PDF:
    read_text = scan_pdf_file(file_bytes)

  return Receipt(filename=uploaded_file.name, text=read_text, timestamp=datetime.now())


def scan_image_file(image_bytes: bytes) -> str:
  image = Image.open(io.BytesIO(image_bytes))
  return pytesseract.image_to_string(image)


def scan_pdf_file(pdf_bytes: bytes) -> str:
  pdf_data = PdfReader(io.BytesIO(pdf_bytes))
  pdf_string = ""
  for page in pdf_data.pages:
    pdf_string += page.extract_text() + "\n"
  return pdf_string
