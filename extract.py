import pytesseract
import cv2
import pdf2image


pdf_file = "l1.pdf"
images = pdf2image.convert_from_path(pdf_file)


text = pytesseract.image_to_string(images[0])

print(text.split())
import re

date_1 = r'(\d{4})[-/\.](\d{2})[-/\.](\d{2})'# match date in format "dd/mm/yyyy"
date_pattern = r'(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})'
# date_pattern = r'(\d{1,2})-"q@"-(\d{4})'

match = re.search(date_pattern, text)
match2=re.search(date_1,text)
if match or match2:
    date = match.group()
    if(match2):
        date_1=match2.group()
    print(f"Extracted date: {date}")
else:
    print("No date found in text")