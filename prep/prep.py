import pandas as pd
from .format import Format
from .prep_time import PrepTime


class Prep:

    def __init__(self):
        pass

    @staticmethod
    def data_prep_step_1(price_df: pd.DataFrame, itm_df: pd.DataFrame):
        """
        Formats and Keeps items with more than 1 input
        :param df: raw_df
        :return: clean_df
        """
        format = Format()
        prep_time = PrepTime()
        formatted_price_df = format.format_data(price_df)
        formatted_itm_df = format.format_category(itm_df)
        concat_df =formatted_price_df.merge(formatted_itm_df[['item_id','item_category_id']], on=['item_id'],
                                            how='left')
        assert len(formatted_price_df) == len(concat_df), "df change after merging item category"

        clean_df = prep_time.clean_data_time_series(concat_df)

        return clean_df

    @staticmethod
    def data_prep_step_2(df: pd.DataFrame):
        """
        Fills periodic inputs
        :return:
        """
        grouped_df=df.groupby(['shop_id','item_id'])
        for group_id, g_df in grouped_df :
            print(group_id)

