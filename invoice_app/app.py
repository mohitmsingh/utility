from flask import Flask, request, jsonify
import json
import os
from modules.invoice_generator import generate_invoice
from modules.google_sheet import add_invoice_entry
from modules.utils import calculate_totals

app = Flask(__name__)

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "invoice-config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

@app.route("/generate-invoice", methods=["POST"])
def create_invoice():
    data = request.json
    try:
        items = data.get("items", [])
        company_name = data.get("company_name", config["business_name"])

        # Calculate totals
        subtotal, gst, total = calculate_totals(items, config["gst_rate"])

        # Write to Google Sheet
        add_invoice_entry(config, company_name, items, subtotal, gst, total)

        # Generate PDF invoice
        file_path = generate_invoice(config, company_name, items, subtotal, gst, total)

        return jsonify({
            "status": "success",
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
