from data import Data
from model import LinearRegression
from prep import Format
from visual import Plot3d


if __name__ == '__main__':

    dir='/Users/bea/Data/kaggle/PredictFutureSales'
    data  = Data(dir)
    format = Format()
    train_df = data.read('sales_train.csv')
    itms_df = data.read('items.csv')
    shops_df = data.read('shops.csv')
    itm_cat_df = data.read('item_categories.csv')
    train_df = format.date_format(train_df,'date')
    train_df = format.string_format(train_df,'date',-1)
    train_df = format.string_format(train_df,'shop_id',2)
    plot=Plot3d
    #plot.plot_3d(train_df.loc[train_df.item_id==22154,['shop_id','date_str','item_price']],'date_str','shop_id','item_price','binary')
