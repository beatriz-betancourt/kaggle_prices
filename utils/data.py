from prep import Format
import pandas as pd
import os


class Data():

    def __init__(self, data_dir):
        self._data_dir = data_dir

    def read(self, filename: str):
        ext = filename.split('.')[-1]
        path = os.path.join(self._data_dir, filename)
        if ext == 'csv':
            df = pd.read_csv(path)
            return df
        else:
            print("file type not implemented")

    def read_format(self, filename: str):
        df = self.read(filename)
        col_list = df.columns.tolist()
        if 'shop_id' in col_list:
            df = Format.string_format(df, 'shop_id', 2)
        if 'item_id' in col_list:
            df = Format.string_format(df, 'item_id', 5)

        return df
