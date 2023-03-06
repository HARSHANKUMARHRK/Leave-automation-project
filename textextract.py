import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


text = pytesseract.image_to_string(Image.open('myopd-sample-rx-eng.png'))
print(text)
import re

dates = []

for line in text.splitlines():
    match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', line)
    if match:
        dates.append(match.group())

print(dates)
