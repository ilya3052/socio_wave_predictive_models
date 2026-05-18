from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV


regression_models = {
    'Ridge': RidgeCV(alphas=[0.1, 1.0, 10.0]),
    'Lasso': LassoCV(cv=5),
    'ElasticNet': ElasticNetCV(l1_ratio=0.5, cv=5),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=50, max_depth=3),
}

predictable_variables = ['likes', 'comms', 'reposts']
