from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoLars,BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


class LinearRegression():

    def __init__(self):
        self.models= {'lr': LinearRegression(),
                      'ridge': Ridge(),
                      'lasso': Lasso(),
                       'en': ElasticNet(),
                      'LassoLars': LassoLars(),
                      'BayesianRidge': BayesianRidge(),
                       'RandomForest': RandomForestRegressor(n_estimators=200, criterion='mse',
                                                                        min_samples_leaf=4, min_samples_split=2,
                                                                        n_jobs=-2, random_state=0),
                       'XGBoost': GradientBoostingRegressor()
                      }
