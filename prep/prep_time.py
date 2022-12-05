import pandas as pd
from utils import DataFrameUtils


class PrepTime:

    def __init__(self):
        self._utils = DataFrameUtils()

    def clean_data_time_series(self, df):
        """
        Remove items that do not have more than 1 price at store level
        :param df: Entire dataframe
        :return: df : Clean dataframe
        """
        items_frequency = self.get_counts(df, ['shop_id', 'item_id'], 'date')
        reduce_df = self.split_data(items_frequency, 'date_frq')
        indx = df['item_id'].isin(reduce_df.item_id.unique())
        clean_df = self._utils.filter_idx(df, indx, 'only itms more than 1 count')
        return clean_df

    def split_data(self, df: pd.DataFrame, col_name: str):
        """
        splits utils that has more than 1 occurence in "colname"
        :param df: Dataframe to perform the splitting
        :param col_name: column to test its value
        :return: df
        """
        indx = df[col_name] > 1
        df = self._utils.filter_idx(df, indx, f'{col_name} more than 1')
        return df
    @staticmethod
    def get_list_unique_values(df: pd.DataFrame, col_name: str):
        return df[col_name].unique().tolist()

    @staticmethod
    def get_counts(df: pd.DataFrame, group_list: list, col_name: str):
        """
        Get the len of unique values in col_name of when df is group by group_name
        :param df: pd.Dataframe
        :param col_name: name of column that has the unique values
        :param group_list: name of column for the groupby
        :return: frequency_df a pd.Dataframe with unique values of col_name and its frequency 
        """
        frequency_df = df.groupby(group_list).agg(date_frq=(col_name, 'nunique')).reset_index()

        return frequency_df
    @staticmethod
    def get_min_max_time_intervals(df: pd.DataFrame, col_name: str):
        min = df[col_name].min()
        max = df[col_name].max()
        step = df.loc[df.sort_values(col_name)[col_name] > min, col_name][0]
        return min, max, step

