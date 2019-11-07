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
#
#
#
# def run():
#     pass
#
#
# def handle_single_training_line(line):
#     regex_decide_intervals_or_still = ""
#     match = re.search(regex_decide_intervals_or_still,line, re.I)
#
#
#
# def process_excel_file():
#     df = pd.read_excel('training.xlsx', sheet_name='Plan Szczegółowy')
#     p_today = date.today().strftime('%Y-%m-%d')
#     today = pd.Timestamp(p_today)
#     var = df.loc[df['data'] == today]
#     print(var[1])
#
#
#     # for index,row in df.iterrows():
#     #     print (row["data"])
#
#
#
#
#
#
#
if __name__ == '__main__':
    from strava import StravaAPI

    # start = timer()
    # Strava = StravaAPI("strava_credentials.json")
    result = Strava.get_activities_links(["10/08/2019", "10/09/2019", "10/10/2019", "10/11/2019", "10/12/2019"],
    #                                      "%m/%d/%Y")
    # end = timer()
    # print(end-start)
    # print(result)
    import datetime

    Sh = SheetHandler("credentials.json")

    dt = datetime.datetime.strptime("10/15/19", "%m/%d/%y")

    print(Sh.get_training_for_day(datetime.datetime.today()))
