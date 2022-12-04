import pandas as pd
from Defaults import Defaults

class PrepTime:

    def __init__(self):
        pass

    def clean_data_time_series(self, df):
        """
        Remove items that do not have more than 1 price at store level
        have a periodic time series price

        :param df: Entire dataframe
        :return: df : Clean dataframe
        """

        items_fequency = self.get_frequency(df, ['shop_id','item_id'], 'date')
        reduce_df = self.split_data(items_fequency, 'date_frq')
        indx = df['item_id'].isin(reduce_df.item_id.unique())
        clean_df = df.loc[indx]
        return clean_df

    def split_data(self, df: pd.DataFrame, col_name: str):
        """
        splits data that has more than 1 occurence in "colname"
        :param df: Dataframe to perform the splitting
        :param col_name: column to test its value
        :return: df
        """
        indx = df[col_name] > 1

        return df.loc[indx]

    def get_list_unique_values(self, df: pd.DataFrame, col_name: str):
        return df[col_name].unique().tolist()

    def get_frequency(self, df: pd.DataFrame, group_name: str, col_name: str):
        """
        Get the len of unique values in col_name of when df is group by group_name
        :param df: pd.Dataframe
        :param col_name: name of column that has the unique values
        :param group_name: name of column for the groupby
        :return: frequency_df a pd.Dataframe with unique values of col_name and its frequency 
        """
        frequency_df = df.groupby(group_name).agg(date_frq=(col_name,'nunique')).reset_index()

        return frequency_df
