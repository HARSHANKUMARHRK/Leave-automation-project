import re
import PyPDF2

# Open the PDF file
pdf_file = open('sample.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Get the first page of the PDF file
page = pdf_reader.getPage(0)

# Extract text from the page
text = page.extractText()

# Use regular expressions to search for a date
date_pattern = r'(\d{4})[-/\.](\d{2})[-/\.](\d{2})'
dates = re.findall(date_pattern, text)

# Print the dates
print(dates)

# Close the PDF file
pdf_file.close()
