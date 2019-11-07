import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
from datetime import datetime as dt
from config import google_sheets_config as cfg

# In order to work correctly, the user has to grant access for admin in the document sharing.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


class SheetHandler:
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    DATE_COLUMN_INDEX = 3
    DATE_FIRST_ROW_INDEX = 2
    DATE_FORMAT_STRING = "%m/%d/%y"
    DATE_FIRST_DATE = dt.strptime("09/30/19", DATE_FORMAT_STRING)

    TRAINING_COL_INDEX = 5
    STRAVA_LINK_COL_INDEX = 11

    def __init__(self, credentials_path, sheet_url_id=cfg["spreadsheet_name"], worksheet_index=cfg["spreadsheet_id"]):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.SCOPE)
        self.client = self.get_client()
        self.sheet = self.get_sheet(sheet_url_id, worksheet_index)
        self.first_date = self.get_base_date() if self.DATE_FIRST_DATE is None else self.DATE_FIRST_DATE

    def get_base_date(self):
        dt_str = self.get_date_by_index(self.DATE_FIRST_ROW_INDEX)
        return dt.strptime(dt_str, self.DATE_FORMAT_STRING)

    def calculate_index(self, date_time):
        time_delta = date_time - self.first_date
        days = time_delta.days
        if days > 0:
            return self.DATE_FIRST_ROW_INDEX + days
        return None

    def get_client(self):
        return gspread.authorize(self.credentials)

    def get_sheet(self, sheet_id, worksheet):
        return self.client.open_by_key(sheet_id).get_worksheet(worksheet)

    def get_cell_value(self, row, column):
        return self.sheet.cell(row, column).value

    def get_date_by_index(self, index):
        return self.get_cell_value(index, self.DATE_COLUMN_INDEX)

    def get_training_for_day(self, date_time):
        row_index = self.calculate_index(date_time)
        return self.get_cell_value(row_index, self.TRAINING_COL_INDEX)

    # def get_data():
    #     sheet = client.open_by_key("1VFaVzCuio0jDkXGsPs8Qkdm3oswGwqPPnryoffVsvpM").get_worksheet(1)
    #     data = sheet.get_all_records()  # Get a list of all records
    #     filtered_items = list()
    #     for d in data:
    #         new_item = dict(date=d["data"], training=d["1"], length=d["ob. Specjalistyczny"])
    #         filtered_items.append(new_item)
    #     return filtered_items

    # def get_training_for_specific_date(training_data, date_string="today", format_string="%d/%m/%Y"):
    #     date_time = None
    #     if date_string is not "today":
    #         try:
    #             date_time = dt.strptime(date_string, format_string)
    #         except ValueError:
    #             return None
    #
    #     date_time = dt.today() if date_time is None else date_time
    #     pattern = date_time.strftime("%m/%d/%y")
    #     return list(filter(lambda item: item["date"] == pattern, training_data))[0]
