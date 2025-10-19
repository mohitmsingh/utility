from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_invoice(config, company_name, items, subtotal, gst, total):
    os.makedirs(config["orders_folder"], exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{company_name}_{date_str}_{int(total)}.pdf"
    file_path = os.path.join(config["orders_folder"], file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    if os.path.exists(config["logo_path"]):
        c.drawImage(config["logo_path"], 40, height - 100, width=100, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(160, height - 60, config["business_name"])
    c.setFont("Helvetica", 10)
    c.drawString(160, height - 80, config["business_address"])
    c.drawString(160, height - 95, config["contact_email"])

    y = height - 150
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(380, y, "Total")

    y -= 20
    c.setFont("Helvetica", 10)
    for item in items:
        c.drawString(40, y, item["name"])
        c.drawString(250, y, str(item["quantity"]))
        c.drawString(300, y, f"{item['price']:.2f}")
        c.drawString(380, y, f"{item['quantity'] * item['price']:.2f}")
        y -= 20

    y -= 20
    c.drawString(300, y, "Subtotal:")
    c.drawString(380, y, f"{subtotal:.2f}")
    y -= 20
    c.drawString(300, y, f"GST ({config['gst_rate']}%):")
    c.drawString(380, y, f"{gst:.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, y, "Total:")
    c.drawString(380, y, f"{total:.2f}")

    c.save()
    return file_path