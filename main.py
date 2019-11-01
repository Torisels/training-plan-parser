# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
# from datetime import date
# import re
import zwift_generator as generator

#
# #Test workout generator
# OUTPUT_FILENAME = "test_workout_file"
# WORKOUT_NAME = "Czwartek 60m"
# PARAMETERS_DICT_LIST = [dict(type=generator.WORKOUT_TYPE_STEADY, Duration="1200", Power="0.6")]
# ZWIFT_PATH = "C:/Users/Gustaw/Documents/Zwift/Workouts/875923/"
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
    print("a,bc".split(","))
