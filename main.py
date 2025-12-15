from invoice_generator import create_invoice
import os
import json

# ✅ Zorg dat de map 'invoices' bestaat
invoice_dir = "invoices"
os.makedirs(invoice_dir, exist_ok=True)

# ✅ Basis klantenbestand (kan later uitgebreid worden)
customers_file = "customers.json"
if os.path.exists(customers_file):
    with open(customers_file, "r") as f:
        customers = json.load(f)
else:
    customers = {
        "Jan de Boer": {"address": "Straat 1, Stad", "vat": "NL123456789B01"}
    }

# ✅ Items voor de factuur
items = [
    {"name": "Website bouwen", "price": 500, "quantity": 1},
    {"name": "Onderhoud", "price": 100, "quantity": 2},
    {"name": "Domeinnaam registratie", "price": 15, "quantity": 1},
    {"name": "SSL Certificaat", "price": 50, "quantity": 1},
    {"name": "Hosting (1 jaar)", "price": 120, "quantity": 1},
    {"name": "SEO Optimalisatie", "price": 200, "quantity": 1}
]

# ✅ Bepaal het volgende factuurnummer
existing_files = os.listdir(invoice_dir)
numbers = []
for f in existing_files:
    try:
        if f.startswith("factuur_") and f.endswith(".pdf"):
            numbers.append(int(f.split("_")[1].split(".")[0]))
    except:
        continue
next_number = max(numbers) + 1 if numbers else 1
invoice_path = f"{invoice_dir}/factuur_{next_number:03d}.pdf"

# ✅ Maak de factuur
create_invoice(
    customer="Jan de Boer",
    items=items,
    output_path=invoice_path
)

print(f"✅ Factuur gegenereerd: {invoice_path}")
