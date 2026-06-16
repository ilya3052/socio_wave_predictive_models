import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.core.config import regression_models, predictable_variables
from src.predictive_models.metrics import read_metrics


def train_models_on_groups(groups_ids):
    grouped_data = read_metrics(groups_ids)

    with ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        futures = [
            executor.submit(train_model_on_group, group_id, group_data)
            for group_id, group_data in grouped_data.items()
        ]
    return [future.result() for future in futures]


def train_model_on_group(group_id, group_data):
    data = {group_id: {}}
    for variable in predictable_variables:
        model_result = []
        for model_name in regression_models:
            result = train_model_on_group_data(model_name, regression_models[model_name], variable, group_data)
            model_result.append(result)
        data[group_id][variable] = model_result
    return data


def train_model_on_group_data(name, model, predicted_variable, df):
    try:
        target_col = f"{predicted_variable}_count"

        X = df.drop([target_col], axis=1)
        y = df[target_col].astype(float)

        y_log = np.log1p(y)

        corr = X.join(y).corr(method='spearman')
        target_corr = corr[target_col]

        features = target_corr[(abs(target_corr) > 0.3) &
            (target_corr != 1.0)
            ].dropna().index.tolist()
        if predicted_variable == 'likes' and 'like_view_ratio' in features:
            features.remove('like_view_ratio')

        X = X[features]

        pipe = make_pipeline(
            StandardScaler(),
            model
        )
        scores = cross_val_score(
            pipe,
            X,
            y_log,
            cv=5,
            scoring="r2",
            error_score='raise'
        )

        y_pred_oof_log = cross_val_predict(pipe, X, y_log, cv=5)

        residuals_log = y_log - y_pred_oof_log

        mae_log = np.mean(np.abs(residuals_log))
        rmse_log = np.sqrt(np.mean(residuals_log ** 2))
        residual_std_log = np.std(residuals_log)

        pipe.fit(X, y_log)

        scaler = pipe.named_steps['standardscaler']
        trained_model = pipe.steps[-1][1]

        coef = trained_model.coef_ / scaler.scale_

        intercept = (
                trained_model.intercept_
                - np.sum(trained_model.coef_ * scaler.mean_ / scaler.scale_)
        )

        coefficients = {
            feature: 0 if abs(float(c)) < 1e-8 else round(float(c), 8)
            for feature, c in zip(features, coef)
        }

        return {
            "model": name,

            "r2_mean": round(float(scores.mean()), 3),
            "r2_std": round(float(scores.std()), 3),

            "mae_log": round(float(mae_log), 5),
            "rmse_log": round(float(rmse_log), 5),
            "residual_std_log": round(float(residual_std_log), 5),

            "intercept": round(float(intercept), 5),
            "coefficients": coefficients,

            "features": features,
        }

    except Exception as e:
        print(e)
