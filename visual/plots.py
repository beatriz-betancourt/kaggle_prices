import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


class Plot3d:

    @staticmethod
    def plot_3d(df: pd.DataFrame, item_id: int, x_col: str, y_col: str, z_col: str, color: str):
        """
        Display in 3D the column values from a pd.Dataframe
        :param df: Dataframe that has all information
        :param x_col: column name for x
        :param y_col: column name for y
        :param z_col: column name for z
        :param color: color name for displaying
        :return: nothing
        """
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        indx = df['item_id'] == item_id
        z_line = np.array(df.loc[indx, z_col].values)
        x_line = np.array(df.loc[indx, x_col].values)
        y_line = np.array(df.loc[indx, y_col].values)
        ax.scatter3D(x_line, y_line, z_line, cmap=color)
        plt.show()
