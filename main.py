import io
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas

# Define the PDF template path and output file path
template_path = 'leave.pdf'
output_path = 'output.pdf'
# Define the new data to be appended to the PDF template
new_data = {'first_name': 'John', 'last_name': 'Doe'}
# Load the PDF template as a PdfFileReader object
with open(template_path, 'rb') as template_file:
    template_reader = PdfFileReader(template_file)
    num_pages = template_reader.getNumPages()

    # Create a new PDF file as a PdfFileWriter object
    output_writer = PdfFileWriter()

    # Append each page of the template to the new PDF file
    for i in range(num_pages):
        template_page = template_reader.getPage(i)
        output_writer.addPage(template_page)

    # Add the new data to the first page of the new PDF file
    first_page = output_writer.getPage(0)
    pdf_canvas = canvas.Canvas(io.BytesIO())
    pdf_canvas.drawString(100, 750, f"First Name: {new_data['first_name']}")
    pdf_canvas.drawString(100, 730, f"Last Name: {new_data['last_name']}")
    pdf_canvas.save()
    new_page = PdfFileReader(io.BytesIO(pdf_canvas.getpdfdata())).getPage(0)
    first_page.mergePage(new_page)
    output_writer.addPage(first_page)

    # Write the new PDF file to disk
    with open(output_path, 'wb') as output_file:
        output_writer.write(output_file)
