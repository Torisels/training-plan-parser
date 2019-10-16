# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
# from datetime import date
# import re
# import generate_xml as generator
#
# #Test workout generator
# OUTPUT_FILENAME = "test_workout_file"
# WORKOUT_NAME = "Czwartek 60m"
# PARAMETERS_DICT = [["Steady","1200","0.55","0"],
#                    ["Intervals","5","120","120","0.55","0.5","110","92"],
#                    ["Steady","1200","0.50","93"]]
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
# if __name__ == '__main__':
#     content = generator.generate_workout_file(OUTPUT_FILENAME,WORKOUT_NAME,PARAMETERS_DICT)
#     print(content)


