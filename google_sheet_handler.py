import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import config

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open(config.google_config["spreadsheetname"]).get_worksheet(config.google_config["spreadsheet_id"]) # Open the spreadsheet

data = sheet.get_all_records()  # Get a list of all records
# pprint(data)
row = sheet.row_values(10)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column


pprint(row)