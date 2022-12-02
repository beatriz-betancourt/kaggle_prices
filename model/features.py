import pandas as pd


class Features:
    def __init__(self):
        pass


    def get_price_features(self,df:pd.DataFrame, group_list:list, functs:list):
        """
        Extracts features from item_price using the function that are in the list parameter
        :param df:
        :param group_list: list of cols to group by
        :param functs: list of functions
        :return: features dataframe
        """
        agg_dict={'item_price': [c for c in functs]}
        features_df = df.groupby(group_list).agg(agg_dict)
        features_df.columns = ["_".join(a) for a in features_df.columns.to_flat_index()]
        return features_df.reset_index()

    def get_date_features(self, df:pd.DataFrame, group_list:list):
        """
        Extracts freatures from date column
        :param df:
        :param group_list: list of columns that the dataframe is goupped by
        :return: features df
        """
        features_df = df.groupby(group_list).agg({
            'date': ['first','last','count']
        })
        features_df.columns = ["_".join(a) for a in features_df.columns.to_flat_index()]
        return features_df.reset_index()


    def get_features(self,df:pd.DataFrame):
        """
        Concatenate features into a single dataframe
        :param df:
        :return:
        """
        functions = ['mean','std','count']
        groupby_cols= ['shop_id','item_id']
        price_df=self.get_price_features(df,groupby_cols,functions)
        date_df = self.get_date_features(df,groupby_cols)

        feaures_df= price_df.merge(date_df,on=['shop_id','item_id'],how='inner')
        return feaures_df

    def add_features(self, clean_df:pd.DataFrame, df:pd.DataFrame):
        groupby_cols=['shop_id','item_id']
        features_df = self.get_features(clean_df)
        train_df = df.merge(features_df,on=groupby_cols,how='left').dropna()
        train_df = train_df.drop(columns=['date','date_str','date_last','date_first'])
        return train_df


