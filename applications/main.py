import pandas as pd

from Defaults import Defaults
from prep import Prep
from utils import Data
from utils import Logger
from model import Features, LinearModels, Selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
import os

if __name__ == '__main__':

    dflt = Defaults()
    logger = Logger()
    data = Data(dflt.DATA_DIR)
    prep = Prep()
    features = Features()
    model = LinearModels()
    sel = Selection()
    logger.print_info("Reading input files")
    features_filename = os.path.join(dflt.OUT_DIR, 'features_target.csv')
    if not os.path.exists(features_filename):
        train_df = data.read(dflt.TRAIN_FILENAME)
        itms_df = data.read(dflt.ITEM_FILENAME)
        logger.print_info("Cleaning data")
        clean_df = prep.data_prep_step_1(train_df, itms_df)
        clean_df, target_df = prep.data_prep_step_2(clean_df,train_df)
        logger.print_info("Getting Features")
        features_df = features.get_features(clean_df)
        merged_df = features_df.merge(target_df, how='inner',
                        indicator=True, on=['shop_id', 'item_id'])

        merged_df.to_csv(features_filename)
    else :
        merged_df = data.read(features_filename)
        merged_df.drop(columns=['date_last','_merge'],inplace=True)
    target_col = 'last_item_price'
    group_features_df = merged_df.groupby(['shop_id', 'item_id'])
    logger.print_info(f"Training Items : {len(group_features_df)}")

    if Defaults.SERIAL:
        save_indicator=0
        score_df = pd.DataFrame()
        for (shop_id, itm_id), group_df in group_features_df:
            if len(group_df) > dflt.MIN_DATA_POINTS:
                X_train, X_test, y_train, y_test = sel.train_test_split_next_value(group_df, target_col,2)
                [model_name, score, best_model] = model.train_test_all_models(X_train,X_test,y_train,y_test)
                model.save_model_joblib(shop_id, itm_id,
                                        best_model, dflt.OUT_DIR, dflt.RUN_INDICATOR)
                score_df = model.append_data_score(shop_id,itm_id,score,score_df)
                if save_indicator % 10 == 0:
                    logger.print_info(f"===> Saving score data for shop_id: {shop_id}")
                    model.save_score(score_df, dflt.OUT_DIR, dflt.RUN_INDICATOR)
                    score_df = pd.DataFrame()
                save_indicator+=1
                logger.print_info(f"shop_id: {shop_id} item_id: {itm_id} {model_name} : {score}")

    else :
        pipe, params = model.set_training_parameters()
        grid_search = GridSearchCV(pipe, param_grid=params, scoring=make_scorer(mean_squared_error))

    logger.print_info("Finish training")
