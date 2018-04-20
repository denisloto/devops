import pandas as pd

class Common():
    def __init__(self):
        pass

    @staticmethod
    def find_developer(developer_code):
        # nameCode,developerName
        df_dev_name = pd.read_csv("dev_name.txt", header=0)
        df= df_dev_name[df_dev_name.nameCode==developer_code]
        if df.empty:
            return ''
        else:
            # print(df)
            return df.iloc[0,1]
