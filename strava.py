import requests
import os
import json
import datetime
import urllib.parse
import pytz
import oauth2


class StravaAPI:
    ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
    ACTIVITIES_URL_WEB = "https://www.strava.com/activities/"
    ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
    DATE_STRING_FORMAT = "%Y-%m-%d"

    def __init__(self, credentials_path, format_string="%d/%m/%Y", token=None):
        self.credentials_path = credentials_path
        self.date_format = format_string
        self.token = token
        if self.token is None:
            oa = oauth2.StravaOAuth(self.credentials_path)
            if oa.check_credentials() is True:
                if self.get_credentials_from_file() is False:
                    raise Exception("Bad file format!")
            else:
                raise Exception("Couldn't log in to Strava")
        else:
            if self.check_token_validity(self.token) is False:
                raise Exception("Please provide valid access token!")

    def get_credentials_from_file(self):
        with open(self.credentials_path, "r") as f:
            data = json.load(f)
            try:
                self.token = data["access_token"]
            except KeyError:
                print("Please provide valid credentials file!")
                return False

    def list_all_activities(self):
        return self.call_strava_api_by_get(self.ACTIVITIES_URL)

    def list_all_activities_in_specific_interval(self, interval_start, interval_end):
        """
        :param interval_end:
        :rtype: dict from json
        :type interval_start: datetime.datetime
        :type interval_end: datetime.datetime
        :type format_string: str
        """
        timestamp_start = interval_start.timestamp()
        timestamp_end = interval_end.timestamp()
        url_params_dict = dict(after=timestamp_start, before=timestamp_end)
        return self.__call_activities(url_params_dict)

    def get_activity_urls_in_specific_interval(self, interval_start, interval_end, format_string=None):
        ret = list()
        activities_dict = self.list_all_activities_in_specific_interval(interval_start, interval_end)

    def __call_activities(self, params_dict=None):
        url = self.ACTIVITIES_URL
        if params_dict is not None:
            url_parameters = urllib.parse.urlencode(params_dict)
            url = ''.join([url, "?", url_parameters])
        return self.call_strava_api_by_get(url)

    def get_activity_id_for_day(self, date_time):
        dt_start = date_time - datetime.timedelta(days=1)
        dt_end = date_time + datetime.timedelta(days=1)
        result = self.list_all_activities_in_specific_interval(dt_start, dt_end)
        proper_date = self.datetime_to_strava_format(date_time)
        for item in result:
            if item['start_date'].split("T")[0] == proper_date:
                return str(item['id'])
        return None

    def get_activity_link_for_day(self, date_time):
        return ''.join([self.ACTIVITIES_URL_WEB, self.get_activity_id_for_day(date_time)])

    def call_strava_api_by_get(self, url):
        """
        This function returns dict for successful call to API or None if status code != 200

        :type url: str
        :rtype: dict
        """
        response = requests.get(url, headers={'Authorization': f'Bearer {self.token}'})
        if response.status_code != 200:
            return None
        return json.loads(response.content.decode("UTF-8"))

    @staticmethod
    def datetime_from_string(d_str, f_str="%d/%m/%Y"):
        """

        :param d_str: str
        :param f_str: str
        :return: datetime.datetime
        """
        return datetime.datetime.strptime(d_str, f_str)

    @staticmethod
    def datetime_to_timestamp(date_string, format_string):
        return datetime.datetime.strptime(date_string, format_string).timestamp()

    @staticmethod
    def datetime_to_strava_format(date):
        """

        :type date: datetime.datetime
        :rtype: str
        """
        return date.strftime("%Y-%m-%d")

    @staticmethod
    def strava_date_to_date_string(strava_date, date_format):
        """

        :rtype: str
        :param date_format: blablabla
        :type strava_date: str
        """
        d = datetime.datetime.strptime(strava_date, StravaAPI.DATE_STRING_FORMAT)
        return d.strftime(date_format)

    @staticmethod
    def get_timestamps_for_certain_day(dt):
        try:
            pst = pytz.timezone("Europe/Warsaw")
            dt = pst.localize(dt)
            utc = pytz.UTC
            dt = dt.astimezone(utc)
            date_after = dt - datetime.timedelta(days=1)
            date_before = dt + datetime.timedelta(days=1)

            return dict(before=int(date_before.timestamp()), after=int(date_after.timestamp()))
        except ValueError:
            return None

    @staticmethod
    def check_token_validity(token):
        response = requests.get(StravaAPI.ATHLETE_URL,
                                headers={'Authorization': f'Bearer {token}'})
        return response.status_code == 200
