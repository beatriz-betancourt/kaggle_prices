import pandas as pd
from .logger import Logger


class DataFrameUtils:

    def __init__(self):
        self._logger = Logger()

    def filter_idx(self, df: pd.DataFrame, logic, tag:str):
        ini_len = len(df)
        df = df.loc[logic]
        final_len = len(df)
        self._logger.print_size_change(ini_len, final_len, f'filter_{tag}')
        return df

    def merge(self, df_1: pd.DataFrame, df_2: pd.DataFrame, on: list, how: str, tag: str):
        ini_len = len(df_1)
        df = df_1.merge(df_2, on=on, how=how)
        final_len = len(df_1)
        self._logger.print_size_change(ini_len, final_len, f"merge_{tag}")
        return df

    def flat_multindex(self, df: pd.DataFrame):
        df.columns = ["_".join(a) for a in df.columns.to_flat_index()]
        return df
