import os.path


class Defaults:

    DATA_DIR = '/home/bea/PycharmProjects/Data/predict_future_sales'
    OUT_DIR = '/data/bea/Data/kaggle/kaggle_prices'
    REPO_DIR = '/home/bea/PycharmProjects/kaggle_prices'
    TRAIN_FILENAME = 'sales_train.csv'
    ITEM_FILENAME = 'items.csv'
    SHOPS_FILENAME = 'shops.csv'
    CATEGORIES_FILENAME = 'item_categories.csv'
    SERIAL = True

    #Training Data Parameters
    RUN_INDICATOR = '1'
    MIN_DATA_POINTS = 3
    #TARGET_COL_NAME = 'item_price'
    TARGET_COL_NAME = 'item_price_last'

    GROUP_BY_COL_NAMES = ['shop_id','item_id']

