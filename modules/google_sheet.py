import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

def add_invoice_entry(config, company_name, items, subtotal, gst, total):
    SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
    if not SERVICE_ACCOUNT_JSON:
        raise Exception("SERVICE_ACCOUNT_JSON environment variable not set")

    creds_dict = json.loads(SERVICE_ACCOUNT_JSON)

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(config["google_sheet_id"]).worksheet(config["sheet_name"])

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [date, company_name, str(items), subtotal, gst, total]
    sheet.append_row(row)
