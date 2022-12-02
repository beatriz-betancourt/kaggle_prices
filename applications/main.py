from data import Data
from prep import Prep
from Defaults import Defaults
from model import Features, LinearModels
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer


if __name__ == '__main__':

    dflt = Defaults()
    data = Data(dflt.DATA_DIR)
    prep = Prep()
    model = LinearModels()
    features = Features()

    train_df = data.read(dflt.TRAIN_FILENAME)
    itms_df = data.read(dflt.ITEM_FILENAME)

    clean_df = prep.data_prep_step_1(train_df, itms_df)
    features_df = features.add_features(clean_df, train_df)
    target_col = dflt.TARGET_COL_NAME
    group_features_df = features_df.groupby(dflt.GROUP_BY_COL_NAMES)

    if Defaults.SERIAL:
        pipe, params = model.set_training_parameters()
        grid_search = GridSearchCV(pipe, param_grid=params, scoring=make_scorer(mean_squared_error))
        for (shop_id, itm_id), group_df in group_features_df:
            if len(group_df) > dflt.MIN_DATA_POINTS :
                y_df = group_df[target_col]
                X_df = group_df.drop(columns=[target_col,dflt.GROUP_BY_COL_NAMES])
                X_train, X_test, y_train, y_test = train_test_split(X_df, y_df, test_size=0.3)
                best_model = grid_search.fit(X_train, y_train)
                y_pred = best_model.predict(X_test)
                model.save_test_score_data(shop_id, itm_id, dflt.REPO_DIR, y_pred, y_test, dflt.RUN_INDICATOR)
                print(grid_search.best_score_)
