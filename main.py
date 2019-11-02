# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
# from datetime import date
import re
import pathlib
import os.path
from os import path
from zwift_generator import ZwiftGenerator as ZG

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
    zwift_gen = ZG(workout_type=ZG.WORKOUT_TYPE_STEADY, zwift_path=ZWIFT_PATH)
    print(zwift_gen.generate_workout_file(ZWIFT_PATH + OUTPUT_FILENAME, WORKOUT_NAME, PARAMETERS_DICT_LIST))
    # regex = r"((<workout_file>)|(<\/.*?>)|(<\w*?\s\/>))"
    #
    # test_str = "<workout_file><author>Gustaw D.</author><name>Test_String</name><description /><sportType>bike</sportType><tags><tag name=\"Created by Python generator by @Torisels\" /></tags><workout><SteadyState Cadence=\"92\" Duration=\"1200\" Pace=\"0\" Power=\"0.6\" /></workout></workout_file>"
    # p = re.compile(regex)
    # print(p.sub(r'\g<1>\n', test_str))
    # path = pathlib.Path(ZWIFT_PATH)
    # print(path.is_dir())
