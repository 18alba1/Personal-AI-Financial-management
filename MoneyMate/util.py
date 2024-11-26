from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import io
import base64

def convert_bytes_to_text(file_bytes):
    # Decode base64 string to bytes
    decoded_bytes = base64.b64decode(file_bytes)
    
    try:
        # First try to open as image
        image = Image.open(io.BytesIO(decoded_bytes))
        # Use pytesseract to extract text from image
        text = pytesseract.image_to_string(image)
        return text
    except:
        try:
            # If not an image, try as PDF
            pdf_data = PdfReader(io.BytesIO(decoded_bytes))
            # receipt data should only have one page
            page = pdf_data.pages[0]
            return page.extract_text()
        except Exception as e:
            return f"Error processing file: {str(e)}"
        
def encode_image(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    return base64.b64encode(file_bytes)