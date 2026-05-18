import os
from concurrent.futures import ProcessPoolExecutor

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.core.config import regression_models, predictable_variables
from src.predictive_models.metrics import read_metrics


def train_model(groups_ids):
    grouped_data = read_metrics(groups_ids)

    with ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        futures = [
            executor.submit(train_group, group_id, group_data)
            for group_id, group_data in grouped_data.items()
        ]
    return futures


def train_group(group_id, group_data):
    data = {group_id: {}}
    for variable in predictable_variables:
        model_result = []
        for model_name in regression_models:
            result = train_model_on_data(model_name, regression_models[model_name], variable, group_data)
            model_result.append(result)
        data[group_id][variable] = model_result
    return data


def train_model_on_data(name, model, predicted_variable, df):
    try:

        X = df.drop([f'{predicted_variable}_count'], axis=1)
        y = df[f'{predicted_variable}_count']

        corr = X.join(y).corr(method='spearman')
        target_corr = corr[f"{predicted_variable}_count"]
        features = target_corr[
            (target_corr.abs() > 0.3) & (target_corr != 1.0)
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
            y,
            cv=5,
            scoring="r2"
        )
        return {
            "model": name,
            "r2_mean": scores.mean(),
            "r2_std": scores.std()
        }
    except Exception as e:
        print(e)
