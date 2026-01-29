from invoice_generator import create_invoice
import os
import json
import sys

# Zorg dat de map 'invoices' bestaat
invoice_dir = "invoices"
os.makedirs(invoice_dir, exist_ok=True)

# Basis klantenbestand
customers_file = "customers.json"
if os.path.exists(customers_file):
    with open(customers_file, "r", encoding="utf-8") as f:
        customers = json.load(f)
else:
    customers = {
        "Jan de Boer": {"address": "Straat 1, Stad", "vat": "NL123456789B01"}
    }

# Items voor de factuur
items = [
    {"name": "Website bouwen", "price": 500, "quantity": 1},
    {"name": "Onderhoud", "price": 100, "quantity": 2},
    {"name": "Domeinnaam registratie", "price": 15, "quantity": 1},
    {"name": "SSL Certificaat", "price": 50, "quantity": 1},
    {"name": "Hosting (1 jaar)", "price": 120, "quantity": 1},
    {"name": "SEO Optimalisatie", "price": 200, "quantity": 1}
]

# Kies klant: eerst CLI-argument, anders default
default_customer = "Jan de Boer"
customer_arg = sys.argv[1] if len(sys.argv) > 1 else None
if customer_arg:
    if customer_arg in customers:
        customer = customer_arg
    else:
        print(f"⚠️ Klant '{customer_arg}' niet gevonden in {customers_file}; gebruik standaard '{default_customer}'.")
        customer = default_customer
else:
    customer = default_customer

# Bepaal volgend factuurnummer
existing_files = os.listdir(invoice_dir)
numbers = []
for f in existing_files:
    try:
        if f.startswith("factuur_") and f.endswith(".pdf"):
            numbers.append(int(f.split("_")[1].split(".")[0]))
    except Exception:
        continue
next_number = max(numbers) + 1 if numbers else 1
invoice_path = os.path.join(invoice_dir, f"factuur_{next_number:03d}.pdf")

# Maakt de factuur aan
create_invoice(
    customer=customer,
    items=items,
    output_path=invoice_path
)

print(f"✅ Factuur gegenereerd: {invoice_path} (Klant: {customer})")
