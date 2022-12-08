import pandas as pd
from utils import Data
from Defaults import Defaults
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error as mse
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import make_scorer
import os
import pickle
import joblib


class LinearModels():

    def __init__(self):
        self.models = {'lr': LinearRegression(),
                       'ridge': Ridge(),
                       'lasso': Lasso(),
                       'en': ElasticNet(),
                       'lassoLars': LassoLars(),
                       'bayesianRidge': BayesianRidge(),
                       'randomForest': RandomForestRegressor(n_estimators=200, criterion='squared_error',
                                                             min_samples_leaf=4, min_samples_split=2,
                                                             n_jobs=-2, random_state=0),
                       'XGBoost': GradientBoostingRegressor()
                       }
        self.data_obj = Data(Defaults.OUT_DIR)

    def get_models(self, type: str):
        return self.models.get(type)

    def save_model(self, shop_id: str, itm_id: str, best_model: GridSearchCV, data_dir: str):
        filename = shop_id + "_" + itm_id + "_model.pkl"
        path_dir = os.path.join(data_dir, 'models')
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        with open(os.path.join(path_dir, filename), 'wb') as file:
            pickle.dump(best_model, file=file)

    def save_model_joblib(self, shop_id: str, itm_id: str, best_model,
                          data_dir: str, run_id: str):
        filename = f"{shop_id}_{itm_id}_{run_id}_model.joblib"
        path_dir = os.path.join(data_dir, 'models')
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        joblib.dump(best_model, os.path.join(path_dir, filename))

    def open_model_joblib(self, shop_id: str, itm_id: str, best_model: GridSearchCV,
                          data_dir: str, run_id: str):
        filename = shop_id + "_" + itm_id + run_id + "_model.joblib"
        path_dir = os.path.join(data_dir, 'models')
        model = joblib.load(os.path.join(path_dir, filename))

        return model

    def open_model(self, shop_id: str, itm_id: str, data_dir: str):
        filename = shop_id + "_" + itm_id + "_model.pkl"
        path_dir = os.path.join(data_dir, 'models')
        if os.path.exists(path_dir):
            with open(os.path.join(path_dir, filename), 'rb') as file:
                model = pickle.load(file)
        else:
            print(f"File {filename} not found")

        return model

    def append_data_score(self, shop_id: str, itm_id: str, score:float,
                        data_score_df:pd.DataFrame):
        if data_score_df.empty:
            data_score_df = pd.DataFrame([[shop_id, itm_id, score]], columns=['shop_id', 'item_id', 'mse'])
        else:
            data = pd.DataFrame([[shop_id, itm_id, score]], columns=['shop_id', 'item_id', 'mse'])
            data_score_df = pd.concat([data_score_df,data], axis=0)
        return data_score_df
    def set_training_parameters_prev(self):
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('model', GeneralModel())
        ])
        params = [
            {
                'model__estimator': [self.get_models('lr')]
            },
            {
                'model__estimator': [self.get_models('ridge')]
            },
            {
                'model__estimator': [self.get_models('randomForest')]
            }
        ]
        return pipe, params

    def set_training_parameters_single_model(self, model_name: str):
        pipe = self.set_training_parameters_pipeline(model_name)
        params = {
            'features__k': [5, 10]
        }
        return pipe, params

    def set_training_parameters_pipeline(self, model_name:str):
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('features', SelectKBest(k=10)),
            ('model', self.get_models(model_name))
        ])
        return pipe

    def get_score_test(self, X_test: pd.DataFrame, y_test: pd.DataFrame, model):
        y_pred = model.predict(X_test)
        score_value = mse(y_test, y_pred)
        return score_value

    def train_test_all_models(self, X_train_df: pd.DataFrame, X_test_df: pd.DataFrame,
                              y_train_df: pd.DataFrame, y_test_df):

        scores_list = []
        for key in self.models.keys():
            pipe = self.set_training_parameters_pipeline(key)
            model = pipe.fit(X_train_df, y_train_df)
            score = self.get_score_test(X_test_df, y_test_df, model)
            scores_list.append([key, score, model])

        score_df = pd.DataFrame(scores_list, columns=['model_name','score','model'])
        best_model =scores_list[score_df.score.argmax()]

        return best_model

    def save_score(self, data:pd.DataFrame, data_dir, tag):
        filename = f"test_score_{tag}.csv"
        path_dir = os.path.join(data_dir, 'info_data')
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        full_path = os.path.join(path_dir, filename)
        if not os.path.exists(full_path):
            data.to_csv(full_path)
        else:
            self.data_obj._data_dir=path_dir
            prev_data = self.data_obj.read_format(filename)
            new_data = pd.concat([prev_data, data], axis=0)
            new_data.to_csv(full_path)



class GeneralModel(BaseEstimator):
    def __init__(self, estimator=LinearRegression()):
        " A custom BaseEstimator"
        self.estimator = estimator

    def fit(self, X, y=None, **kwargs):
        self.estimator.fit(X, y)
        return self

    def predict(self, X):
        return self.estimator.predict(X)

    def score(self, X, y):
        return self.estimator.score(X, y)
