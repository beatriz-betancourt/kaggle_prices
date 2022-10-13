from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

class Plot3d():

        @staticmethod
        def plot_3d(df,x_col,y_col,z_col,color):
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            z_line=df[z_col].values
            x_line=df[x_col].values
            y_line=df[y_col].values
            ax.scatter3D(x_line,y_line,z_line,cmap=color)
            plt.show()

