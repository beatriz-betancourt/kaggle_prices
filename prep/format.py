import pandas as pd


class Format():

    @staticmethod
    def string_format(df: pd.DataFrame, colname: str, max: int):
        """
        Pads with "max" zeros, format columns to strings,
        and rename columns names base on max parameter
        if max == -1 it doesn't pad with zeros
        :param df: pd.Dataframe
        :param colname: name of the columns
        :param max: number of zeros to pad the column
        :return: pd.Dataframe
        """

        if max == -1:
            colname_new = colname + "_str"
            df.loc[:, colname_new] = df.loc[:, colname].astype(str)
        else:
            df.loc[:, colname] = df.loc[:, colname].astype(str).str.zfill(max)
        return df

    def date_format(self, df: pd.DataFrame, colname: str):
        """
        Format to datetime a column that is in string format
        :param df: pd.Dataframe
        :param colname: columns name
        :return:
        """

        df.loc[:, colname] = pd.to_datetime(df.loc[:, colname], infer_datetime_format=True, dayfirst=True)
        return df

    def format_data(self, df:pd.DataFrame):
        """
        Prepare data types for training
        :param df:
        :return: df
        """
        df = self.date_format(df, 'date')
        df = self.string_format(df, 'date', -1)
        df = self.string_format(df, 'shop_id', 2)
        df = self.string_format(df, 'item_id', 5)

        return df

    def format_category(self, df:pd.DataFrame):
        """
        Format category datafile
        :param df:
        :return:
        """
        df = self.string_format(df, 'item_category_id', 2)
        df = self.string_format(df, 'item_id', 5)
        return df