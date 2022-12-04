import pandas as pd
from .format import Format
from .prep_time import PrepTime


class Prep:

    def __init__(self):
        pass

    @staticmethod
    def data_prep_step_1(price_df: pd.DataFrame, itm_df: pd.DataFrame):
        """
        Formats columns, appends itm_df, and keeps items that have more than 1 time input
        :param price_df: raw price df
        :param itm_df: item information
        :return: clean_df
        """
        format_obj = Format()
        formatted_price_df = format_obj.format_data(price_df)
        formatted_itm_df = format_obj.format_category(itm_df)
        concat_df = formatted_price_df.merge(
            formatted_itm_df[['item_id', 'item_category_id']], on=['item_id'], how='left')
        assert len(formatted_price_df) == len(concat_df), "df change after merging item category"

        return concat_df

    @staticmethod
    def data_prep_step_2(df: pd.DataFrame):
        """
        Cleans time dependence variables and fills in periodic inputs
        :return:
        """
        prep_time = PrepTime()
        clean_df = prep_time.clean_data_time_series(df)

        return clean_df

    @staticmethod
    def data_prep_step_3(df: pd.DataFrame):
        """

        :param df:
        :return:
        """
        prep_time = PrepTime()
        prep_time.set_same_time_period(df)