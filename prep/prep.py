import pandas as pd
from .format import Format
from .prep_time import PrepTime
import os
from Defaults import Defaults


class Prep:

    def __init__(self):
        self.dflts = Defaults()

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

    def data_prep_step_2(self, clean_df: pd.DataFrame, train_df: pd.DataFrame):
        """
        Cleans time dependence variables, remove items that have less than 1 counts
        To use at shop_id, item_id level
        :param clean_df:
        :param train_df: raw_df
        :return:
        """
        filename = os.path.join(self.dflts.OUT_DIR, 'single_count_items.csv')
        items_one_df, rest_df = self.remove_unique_items(train_df)
        if not os.path.exists(filename):
            items_one_df.to_csv(filename)
        clean_df, target_df = self.remove_last_price(clean_df)

        return clean_df, target_df

    @staticmethod
    def remove_unique_items(df: pd.DataFrame):
        """
        removes items that have only one occurrence
        :param df:
        :return:
        """
        group_df = df.groupby(['shop_id', 'item_id']).agg(
            {'date': ['count', 'last']})
        group_df.columns = ['date_count', 'date_last']
        indx = group_df['date_count'] < 3
        unique_df = group_df.loc[indx]
        no_unique_df = group_df.loc[~indx].reset_index()
        clean_df = df.merge(no_unique_df[['shop_id', 'item_id']],
                            how='inner', on=['shop_id', 'item_id'])
        col_names = df.columns.to_list()
        clean_df = clean_df.loc[:,col_names]
        return unique_df.reset_index(), clean_df

    def remove_last_price(self, clean_df: pd.DataFrame):
        """
        Remove last price for training and separated them in a test_df
        :param clean_df:
        :return: clean_df, test_df
        """
        ordered_df = clean_df.sort_values(by=['shop_id', 'item_id', 'date']).reset_index()
        group_df = ordered_df.groupby(['shop_id', 'item_id']).agg(
            {'date': ['count', 'last'], 'item_price': ['last']})
        group_df.columns = ['date_count', 'date_last', 'last_item_price']

        clean_df['date_str'] = clean_df['date'].astype(str)
        group_df['date_str'] = group_df['date_last'].astype(str)
        merged_df = clean_df.merge(group_df, how='left', on=['shop_id', 'item_id', 'date_str'], indicator=True)
        indx = merged_df['_merge'] == 'both'
        test_df = merged_df.loc[indx, ['shop_id', 'item_id', 'last_item_price', 'date_last']]
        col_list = clean_df.columns.to_list()
        clean_df = merged_df.loc[~indx, col_list]
        return clean_df, test_df
