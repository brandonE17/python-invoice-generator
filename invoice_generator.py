from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

from config import LOGO_PATH, COMPANY_NAME, COMPANY_SIGNATORY
   
def draw_logo(c, width, height, logo_width=80, top_offset=180):
    
 
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        x = width - logo_width - 50
        y = height - top_offset
        c.drawImage(
            ImageReader(LOGO_PATH),
            x,
            y,
            width=logo_width,
            preserveAspectRatio=True,
            mask='auto'
        )

        def draw_header(c, width, height, customer, invoice_number):

            #title
            c.setFont("Helvetica-Bold", 22)
            c.drawString(50, height - 100, "FACTUUR") 

            #customer & company info
            c.setFont("Helvetica", 11)
            c.drawString(50, height - 130, f"Klant: {customer}")
            c.drawString(50, height - 150, f"Bedrijf: {COMPANY_NAME}")

            #invoice metadata (right aligned)
            invoice_date = datetime.now().strftime("%d-%m-%Y")  
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 50, height - 130, f"Factuurnummer: {invoice_number}")
            c.drawRightString(width - 50, height - 145, f"Factuurdatum: {invoice_date}")

            #divider line
            c.line(50, height - 185, width - 50, height - 185)


    def draw_items_table(c, width, height, items):
        y = height - 220
        total = 0

        # Table header
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Omschrijving")
        c.drawString(width - 300, y, "Aantal")
        c.drawString(width - 200, y, "Prijs (€)")
        c.drawString(width - 100, y, "Totaal (€)")
        y -= 20
        c.line(50, y, width - 50, y)
        y -= 10

        c.setFont("Helvetica", 11)
        for item in items:
            aantal = item.get("quantity", 1)
            totaal_item = item["price"] * aantal


            c.drawString(50, y, item["name"])
            c.drawString(width - 300, y, str(aantal))
            c.drawString(width - 200, y, f"{item['price']:.2f}")
            c.drawString(width - 100, y, f"{totaal_item:.2f}")

            total += totaal_item
            y -= 20

        return total, y 
    
    

    def draw_totals(c, width, subtotal, y):

        vat= subtotal * 0.21
        total = subtotal + vat

        y -= 10
        c.line(width - 200, y, width - 50, y)
        y -= 15 

        c.setFont("Helvetica-Bold", 11)
        c.drawString(width - 200, y, "Subtotaal:")
        c.drawString(width - 100, y, f"€{subtotal:.2f}")

        y -= 20
        c.drawString(width - 200, y, "BTW (21%):")
        c.drawString(width - 100, y, f"€{vat:.2f}")

        y -= 20
        c.drawString(width - 200, y, "Totaal:")
        c.drawString(width - 100, y, f"€{total:.2f}")



def draw_footer(c, width):
    """
    Draws footer text.
    """
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(
        width / 2,
        60,
        "Dit document is automatisch gegenereerd en heeft geen handtekening nodig."
    )
    c.drawCentredString(
        width / 2,
        45,
        f"Automatisch gegenereerd namens {COMPANY_NAME} – {COMPANY_SIGNATORY}"
    ) 


def create_invoice(customer, items, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    #  Logo rechtsboven
    draw_logo(c, width, height)

    #  Titel
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 100, "FACTUUR")

    # Info
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 130, f"Klant: {customer}")
    c.drawString(50, height - 150, f"Datum: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(50, height - 170, f"Bedrijf: {COMPANY_NAME}")

    c.line(50, height - 185, width - 50, height - 185)

    # Items in tabel
    y = height - 220
    total = 0

    # Kop van de tabel
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Omschrijving")
    c.drawString(width - 300, y, "Aantal")
    c.drawString(width - 200, y, "Prijs (€)")
    c.drawString(width - 100, y, "Totaal (€)")
    y -= 20
    c.line(50, y, width - 50, y)
    y -= 10

    c.setFont("Helvetica", 11)
    for item in items:
        aantal = item.get("quantity", 1)
        totaal_item = item["price"] * aantal
        c.drawString(50, y, item["name"])
        c.drawString(width - 300, y, str(aantal))
        c.drawString(width - 200, y, f"{item['price']:.2f}")
        c.drawString(width - 100, y, f"{totaal_item:.2f}")
        total += totaal_item
        y -= 20

    # Lijn boven de totalen
    y -= 10
    c.line(width - 200, y, width - 50, y)
    y -= 15

    #  Totals
    btw = total * 0.21
    c.setFont("Helvetica-Bold", 11)
    c.drawString(width - 200, y, "Subtotaal:")
    c.drawString(width - 100, y, f"€{total:.2f}")
    y -= 20
    c.drawString(width - 200, y, "BTW (21%):")
    c.drawString(width - 100, y, f"€{btw:.2f}")
    y -= 20
    c.drawString(width - 200, y, "Totaal:")
    c.drawString(width - 100, y, f"€{total + btw:.2f}")

    #  Digitale ondertekeningssectie
    y_sign = 140
    c.setLineWidth(0.8)
    c.line(width / 2 - 180, y_sign, width / 2 - 20, y_sign)
    c.drawCentredString(width / 2 - 100, y_sign - 15, "Namens bedrijf")
    c.line(width / 2 + 20, y_sign, width / 2 + 180, y_sign)
    c.drawCentredString(width / 2 + 100, y_sign - 15, "Namens klant")

    #  Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, 60,
                        "Dit document is automatisch gegenereerd en heeft geen handtekening nodig.")
    c.drawCentredString(width / 2, 45,
                        f"Automatisch gegenereerd namens {COMPANY_NAME} – {COMPANY_SIGNATORY}")

    c.save()
