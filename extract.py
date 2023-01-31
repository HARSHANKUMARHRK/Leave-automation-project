import pytesseract
import cv2
import pdf2image

# convert pdf to image
pdf_file = "doctor.pdf"
images = pdf2image.convert_from_path(pdf_file)

# use OCR to extract text from image
text = pytesseract.image_to_string(images[0])

print(text.split())
import re

# extract date from text
date_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}") # match date in format "dd/mm/yyyy"
match = re.search(date_pattern, text)
if match:
    date = match.group()
    print(f"Extracted date: {date}")
else:
    print("No date found in text")

