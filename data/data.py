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
            print("Formatted not implemented")
