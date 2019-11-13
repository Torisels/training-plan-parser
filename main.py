import re
import pathlib
import os.path
from os import path

from zwift_generator import ZwiftGenerator as ZG
from google_sheet_handler import SheetHandler
from timeit import default_timer as timer

#
# #Test workout generator
OUTPUT_FILENAME = "sat_test.zwo"
WORKOUT_NAME = "Saturday_test"
PARAMETERS_DICT_LIST = [dict(type=ZG.WORKOUT_TYPE_STEADY, Duration="1200", Power="0.6", Cadence="90-95")]
ZWIFT_PATH = "C:/Users/Gustaw/Documents/Zwift/Workouts/875923/"


def update_today():
    import datetime
    from strava import StravaAPI
    Strava = StravaAPI("strava_credentials.json")
    Sh = SheetHandler("credentials.json")
    dt = datetime.datetime.today()
    strava_result = Strava.get_activity_id_for_day(dt)
    Sh.update_strava_link(dt, strava_result[0], strava_result[1])


if __name__ == '__main__':
    update_today()

    # print(Sh.get_training_for_day(dt))
    # Sh.update_strava_link(dt,link)
