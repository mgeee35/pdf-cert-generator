from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import secrets
import psycopg2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import openpyxl

# FastAPI application
app = FastAPI()

# CORS Middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Requests from all origins are accepted
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Certificate Data Model
class CertificateData(BaseModel):
    name: str
    type: str
    duration: str
    date: str
    organizer: str

# PostgreSQL connection
def connect_db():
    conn = psycopg2.connect(
        dbname="skymodcert",   # Database name
        user="skymod",         # PostgreSQL username
        password="123456",     # PostgreSQL password
        host="localhost",      # Connection address
        port="5432"            # Connection port
    )
    return conn

# Generate certificate number
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

# Save certificate to Excel
def save_certificate_to_excel(token, link, filename):
    try:
        try:
            workbook = openpyxl.load_workbook(filename)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        sheet = workbook.active
        sheet.append([token, link])  # Add token and link to Excel

        workbook.save(filename)
    except Exception as e:
        print(f"An error occurred: {e}")

# Save certificate to the database
def save_certificate_to_db(token, data, pdf_data):
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the 'certificates' table exists, and create it if not
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS certificates (
        id SERIAL PRIMARY KEY,
        certificate_number VARCHAR(64) UNIQUE NOT NULL,
        candidate_name VARCHAR(255) NOT NULL,
        training_name VARCHAR(255) NOT NULL,
        training_duration VARCHAR(255) NOT NULL,
        training_date DATE NOT NULL,
        pdf BYTEA NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(create_table_query)  # Execute the table creation query

    # Insert the certificate data into the 'certificates' table
    insert_query = '''
    INSERT INTO certificates (
        certificate_number, candidate_name, training_name, 
        training_duration, training_date, pdf
    ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (token, data.name, data.type, data.duration, data.date, psycopg2.Binary(pdf_data)))

    # Commit changes to the database
    conn.commit()

    cursor.close()
    conn.close()


# Certificate creation function
@app.post("/generate_certificate/")
def generate_certificate(data: CertificateData):
    # Generate a unique certificate number
    token = generate_unique_token()

    # Generate the PDF output
    lowercase_name = data.name.lower().replace('ü', 'u').replace('ş', 's').replace('ı', 'i').replace('ö', 'o').replace('ğ', 'g').replace('ç', 'c').replace(' ', '_')
    output_pdf = f"./{lowercase_name}.pdf"
    write_on_pdf(output_pdf, token, data)

    # Read the PDF file as bytes
    with open(output_pdf, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    # Save the certificate to the database
    save_certificate_to_db(token, data, pdf_data)

    # Save the certificate link and token to Excel
    link = f"./{lowercase_name}.pdf"
    save_certificate_to_excel(token, link, "certificate_info.xlsx")

    # Certificate has been successfully generated
    return {"message": "Certificate generated successfully", "certificate_link": link, "token": token}
