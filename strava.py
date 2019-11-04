import requests
import os
import json
import datetime
import urllib.parse
import pytz


class StravaAPI:
    ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
    ACTIVITIES_URL_WEB = "https://www.strava.com/activities/"
    ATHLETE_URL = "https://www.strava.com/api/v3/athlete"

    def __init__(self, credentials_path, format_string="%d/%m/%Y", token=None):
        self.credentials_path = credentials_path
        self.date_format = format_string
        self.token = token
        if os.path.exists(credentials_path) is False:
            raise InterruptedError("Please provide valid credentials' file path!")
        if self.token is not None:
            self.get_credentials()

    def get_credentials(self):
        with open(self.credentials_path, "r") as f:
            data = json.load(f)
            self.token = data["access_token"]

    def list_all_activities(self):
        response = requests.get(self.ACTIVITIES_URL,
                                headers={'Authorization': f'Bearer {self.token}'})
        print(response.json())

    def get_activity_id_for_day(self, date_string):
        timestamps_dict = self.get_timestamps_for_certain_day(date_string, self.date_format)
        url = ''.join([self.ACTIVITIES_URL, "?", urllib.parse.urlencode(timestamps_dict)])
        result = self.call_strava_api(url)
        proper_date = self.get_date_time_in_strava_format(date_string, self.date_format)
        for item in result:
            if item['start_date'].split("T")[0] == proper_date:
                return str(item['id'])
        return None

    def call_strava_api(self, url):
        return requests.get(url, headers={'Authorization': f'Bearer {self.token}'}).json()

    def get_activity_link(self, date):
        return ''.join([self.ACTIVITIES_URL_WEB, self.get_activity_id_for_day(date)])

    @staticmethod
    def get_date_time_in_strava_format(date_string, format_string="%d/%m/%Y"):
        date_time = datetime.datetime.strptime(date_string, format_string)
        return date_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_timestamps_for_certain_day(date_string, format_string="%d/%m/%Y"):
        date_time = None
        if date_string is not "today":
            try:
                pst = pytz.timezone("Europe/Warsaw")
                date_time = datetime.datetime.strptime(date_string, format_string)
                date_time = pst.localize(date_time)
                utc = pytz.UTC
                date_time = date_time.astimezone(utc)
                date_after = date_time - datetime.timedelta(days=1)
                date_before = date_time + datetime.timedelta(days=1)

                return dict(before=int(date_before.timestamp()), after=int(date_after.timestamp()))
            except ValueError:
                return None

    @staticmethod
    def check_token_validity(token):
        response = requests.get(StravaAPI.ATHLETE_URL,
                                headers={'Authorization': f'Bearer {token}'})
        return response.status_code == 200
