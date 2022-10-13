import pandas as pd

class Format():

    def string_format(self,df:pd.DataFrame ,colname:str, max:int):

        if max == -1:
            colname_new=colname+"_str"
            df.loc[:, colname_new] = df.loc[:, colname].astype(str)
        else:
            df.loc[:,colname]=df.loc[:,colname].astype(str).str.zfill(max)
        return df

    def date_format(self,df:pd.DataFrame, colname):

        df.loc[:, colname] = pd.to_datetime(df.loc[:, colname], infer_datetime_format=True, dayfirst=True)
        return df
