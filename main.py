import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from datetime import date



def run():
    pass


def process_excel_file():
    df = pd.read_excel('training.xlsx', sheet_name='Plan Szczegółowy')
    p_today = date.today().strftime('%Y-%m-%d')
    today = pd.Timestamp(p_today)
    var = df.loc[df['data'] == today]
    print(var[1])


    # for index,row in df.iterrows():
    #     print (row["data"])







if __name__ == '__main__':
    process_excel_file()