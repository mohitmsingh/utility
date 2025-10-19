import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), "..", "service_account.json")

def add_invoice_entry(config, company_name, items, subtotal, gst, total):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_PATH, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(config["google_sheet_id"]).worksheet(config["sheet_name"])
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        date,
        company_name,
        str(items),
        subtotal,
        gst,
        total
    ])