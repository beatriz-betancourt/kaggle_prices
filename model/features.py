import pandas as pd
from utils import DataFrameUtils
from prep import PrepTime

class Features:
    def __init__(self):
        self._utils = DataFrameUtils()
        self._prep_time = PrepTime()
    def get_price_features(self, df: pd.DataFrame, group_list: list, functs: list):
        """
        Extracts features from item_price using the function that are in the list parameter
        :param df:
        :param group_list: list of cols to group by
        :param functs: list of functions
        :return: features dataframe
        """
        agg_dict = {'item_price': [c for c in functs]}
        features_df = df.groupby(group_list).agg(agg_dict)
        features_df.columns = ["_".join(a) for a in features_df.columns.to_flat_index()]
        return features_df.reset_index()

    @staticmethod
    def get_date_features(df: pd.DataFrame, group_list: list):
        """
        Extracts features from date column
        :param df:
        :param group_list: list of columns that the dataframe is groupped by
        :return: features df
        """
        features_df = df.groupby(group_list).agg({
            'date': ['first', 'last', 'count', 'nunique']
        })
        features_df.columns = ["_".join(a) for a in features_df.columns.to_flat_index()]
        features_df['date_freq'] = features_df['date_last'] - features_df['date_first']
        features_df['days_freq'] = features_df['date_freq'].apply(lambda x: pd.Timedelta(x).days)

        return features_df.reset_index()

    def get_features(self, df: pd.DataFrame):
        """
        Concatenate features into a single dataframe
        :param df:
        :return:
        """
        functions = ['mean', 'std', 'count','min','max','last','first']
        groupby_cols = ['shop_id', 'item_id']
        price_df = self.get_price_features(df, groupby_cols, functions)
        date_df = self.get_date_features(df, groupby_cols)
        features_df = self._utils.merge(price_df, date_df, on=groupby_cols, how='inner', tag='date_features')
        shift_df = self.get_shift_features(df)
        features_df = self._utils.merge(features_df, shift_df, on=groupby_cols, how='inner', tag='shift_features')
        category_df = df[['item_id','item_category_id']].drop_duplicates()
        features_df = self._utils.merge(features_df, category_df, on=['item_id'],how='left', tag='category_id')
        features_df = features_df.drop(columns=['shop_id', 'item_category_id', 'item_id', 'date_freq',
                                                'date_first', 'date_last']).fillna(0)
        return features_df

    def add_features(self, clean_df: pd.DataFrame, df: pd.DataFrame):
        groupby_cols = ['shop_id', 'item_id']
        features_df = self.get_features(clean_df)
        train_df = df.merge(features_df, on=groupby_cols, how='left').dropna()
        train_df = self.extract_date_columns(train_df)
        return train_df

    def extract_date_columns(self, train_df):
        train_df = train_df.drop(columns=['date', 'date_str', 'date_last', 'date_first', 'date_freq'])
        return train_df

    def get_shift_features(self, df: pd.DataFrame):
        """
        Computes features from the date shift intervals at shop_id, item_id level
        :param df:
        :return:
        """
        group_list = ['shop_id', 'item_id']
        clean_df = self._prep_time.clean_data_time_series(df)
        sorted_df = clean_df.sort_values(by=['shop_id', 'item_id', 'date'])
        sorted_df['next_date'] = sorted_df['date'].shift()
        sorted_df['shift'] = sorted_df['date'] - sorted_df['next_date']
        sorted_df['shift_days'] = sorted_df['shift'].apply(lambda x: pd.Timedelta(x).days)
        filtered_df = self._utils.filter_idx(sorted_df, sorted_df['shift_days'] > 0,'remove initial shift')
        features_df = filtered_df.groupby(group_list).agg({
            'shift_days': ['mean', 'std', 'min', 'max', 'count']})
        features_df = self._utils.flat_multindex(features_df)
        return features_df

    def set_same_time_period(self, df: pd.DataFrame, col_name: str):
        """
        Sets values to get all items the same time period in col_name
        It uses back-filled values based on frequency
        :param df:
        :param col_name: name of column to clean
        :return: df
        """

        group_by_list = ['shop_id', 'item_id']
        shop_itm_df = Features.get_date_features(df, group_by_list)
        shop_itm_df['date_range'] = (shop_itm_df['date_last'] - shop_itm_df['date_first'])
        shop_itm_df['date_freq'] = shop_itm_df['date_range'] / shop_itm_df['date_nunique']
        shop_itm_df['days_freq'] = shop_itm_df['date_freq'].apply(lambda x: pd.Timedelta(x).days)

        return shop_itm_df
