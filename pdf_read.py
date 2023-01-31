from PyPDF2 import PdfFileReader
from PIL import Image
import pytesseract

def extract_date_from_pdf(pdf_file_path):
    # Open the PDF file
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PdfFileReader(pdf_file)

    # Get the first page of the PDF
    page = pdf_reader.getPage(0)

    # Convert the page to an image
    page_image = Image.open(page.to_image())

    # Use OCR to extract text from the image
    text = pytesseract.image_to_string(page_image)

    # Close the PDF file
    pdf_file.close()

    # Extract the date from the extracted text
    # ...

    return text


extract_date_from_pdf("leave_status_21.pdf")
