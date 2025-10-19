import json
import os
import argparse
from modules.invoice_generator import generate_invoice
from modules.google_sheet import add_invoice_entry
from modules.utils import calculate_totals

# Parse payload JSON (from GitHub Actions)
parser = argparse.ArgumentParser()
parser.add_argument("--payload", type=str, required=True, help="Path to JSON payload")
args = parser.parse_args()

with open(args.payload, "r") as f:
    data = json.load(f)

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "invoice-config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

items = data.get("items", [])
company_name = data.get("company_name", config["business_name"])

subtotal, gst, total = calculate_totals(items, config["gst_rate"])

# Update Google Sheet
add_invoice_entry(config, company_name, items, subtotal, gst, total)

# Generate PDF invoice
file_path = generate_invoice(config, company_name, items, subtotal, gst, total)

print(f"Invoice generated: {file_path}")
