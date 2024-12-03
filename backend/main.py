from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import openpyxl
import os
import uuid
from typing import List

# FastAPI application
app = FastAPI()

# Path to the Excel file
filename = 'certificate_info.xlsx'

# Certificate Data Model
class CertificateData(BaseModel):
    name: str
    type: str
    duration: str
    date: str
    organizer: str

# Generate a unique certificate number
def generate_unique_token():
    token = secrets.token_hex(16)  # Generate a hexadecimal token
    return token

# Function to write data to the PDF
def write_on_pdf(output_pdf, token, data):
    reader = PdfReader("template_certificate.pdf")
    writer = PdfWriter()

    pdfmetrics.registerFont(TTFont('Poppins-Regular', './font/Poppins/Poppins-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Poppins-Medium', './font/Poppins/Poppins-Medium.ttf'))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    can.setFont("Poppins-Medium", 16)
    can.drawString(209, 455, f"{token}")  # Certificate number
    can.setFont("Poppins-Medium", 18)

    can.drawString(209, 407, data.name)
    can.drawString(209, 350, data.type)
    can.drawString(209, 290, data.duration)
    can.drawString(209, 230, data.date)
    can.drawString(209, 172, data.organizer)
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Token '{token}' has been written to {output_pdf}.")

# Save the certificate data to Excel
def save_certificate_to_excel(token, link, filename):
    try:
        try:
            workbook = openpyxl.load_workbook(filename)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        sheet = workbook.active
        sheet.append([token, link])  # Add the token and link to the Excel sheet

        workbook.save(filename)
        print(f"Data saved to {filename} with a unique token.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Certificate generation function
@app.post("/generate_certificate/")
def generate_certificate(data: CertificateData):
    # Generate a unique certificate number
    token = generate_unique_token()

    # Create the PDF output
    lowercase_name = data.name.lower().replace('ü', 'u').replace('ş', 's').replace('ı', 'i').replace('ö', 'o').replace('ğ', 'g').replace('ç', 'c').replace(' ', '_')
    output_pdf = f"./{lowercase_name}.pdf"
    write_on_pdf(output_pdf, token, data)

    # Save the certificate link and token to the Excel file
    link = f"./{lowercase_name}.pdf"
    save_certificate_to_excel(token, link, filename)

    # The certificate has been successfully generated
    return {"message": "Certificate generated successfully", "certificate_link": link, "token": token}
