import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_invoice(to_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "Uw factuur"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content("In de bijlage vindt u uw factuur.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="factuur.pdf")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
 