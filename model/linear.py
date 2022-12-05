import pandas as pd
from utils import Data
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error as mse
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import os
import pickle


class LinearModels():

    def __init__(self, data_obj: Data):
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
        self.data_obj = data_obj


    def get_models(self, type: str):
        return self.models.get(type)

    def save_model(self, shop_id: str, itm_id: str, best_model: GridSearchCV, data_dir: str):
        filename = shop_id + "_" + itm_id + "_model.pkl"
        path_dir = os.path.join(data_dir, 'models')
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        with open(os.path.join(path_dir, filename), 'wb') as file:
            pickle.dump(best_model, file=file)

    def open_model(self, shop_id: str, itm_id: str, data_dir: str):
        filename = shop_id + "_" + itm_id + "_model.pkl"
        path_dir = os.path.join(data_dir, 'models')
        if os.path.exists(path_dir):
            with open(os.path.join(path_dir, filename), 'rb') as file:
                model = pickle.load(file)
        else:
            print(f"File {filename} not found")

        return model

    def save_test_score_data(self, shop_id: str, itm_id: str, data_dir: str,
                             y_pred, y_test, tag: str):
        filename = f"test_score_{tag}.csv"
        path_dir = os.path.join(data_dir, 'info_data')
        score = mse(y_test, y_pred)
        data = pd.DataFrame([[shop_id, itm_id, score]], columns=['shop_id', 'item_id', 'mse'])
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        full_path = os.path.join(path_dir, filename)
        if not os.path.exists(full_path):
            data.to_csv(full_path)
        else:
            prev_data = self.data_obj.read_format(filename)
            new_data = pd.concat([prev_data, data], axis=0)
            new_data.to_csv(full_path)

    def set_training_parameters(self):
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
