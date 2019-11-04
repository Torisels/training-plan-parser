import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
import datetime

# In order to work correctly, the user has to grant access for admin in the document sharing.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)


class SheetHandler:
    def get_data():
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1VFaVzCuio0jDkXGsPs8Qkdm3oswGwqPPnryoffVsvpM").get_worksheet(1)
        data = sheet.get_all_records()  # Get a list of all records
        filtered_items = list()
        for d in data:
            new_item = dict(date=d["data"], training=d["1"], length=d["ob. Specjalistyczny"])
            filtered_items.append(new_item)
        return filtered_items

    def get_training_for_specific_date(training_data, date_string="today", format_string="%d/%m/%Y"):
        date_time = None
        if date_string is not "today":
            try:
                date_time = datetime.datetime.strptime(date_string, format_string)
            except ValueError:
                return None

        date_time = datetime.datetime.today() if date_time is None else date_time
        pattern = date_time.strftime("%m/%d/%y")
        return list(filter(lambda item: item["date"] == pattern, training_data))[0]


data = get_data()
print(get_training_for_specific_date(data, "05/11/2019"))
