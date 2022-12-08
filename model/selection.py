import pandas as pd
from sklearn.model_selection import train_test_split


class Selection:

    def __init__(self):
        pass

    @staticmethod
    def train_test_split_next_value(merged_df, col_name: str, len_last:str):
        """
        Splits dataframe in test and training by taking the last occurrence
        :param merged_df: It has to contain col_name
        :param col_name: target columns name
        :return: X_train_df, X_test_df, y_train_df, y_test
        """
        y_df = merged_df[col_name]
        cols_names = merged_df.columns.to_list()
        cols_names.remove(col_name)
        x_train_df = merged_df.iloc[:-len_last].loc[:,cols_names]
        x_test_df = merged_df.loc[:,cols_names].iloc[-len_last:]
        y_train_df = y_df.iloc[:-len_last]
        y_test_df = y_df.iloc[-len_last:]
        return x_train_df, x_test_df, y_train_df, y_test_df

