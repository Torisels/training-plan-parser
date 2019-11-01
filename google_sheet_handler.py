import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

# In order to work correctly, the user has to grant access for admin in the document sharing.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)


def get_data():
    client = gspread.authorize(creds)
    sheet = client.open(config.google_config["spreadsheet_name"]).get_worksheet(config.google_config["spreadsheet_id"])
    data = sheet.get_all_records()  # Get a list of all records
