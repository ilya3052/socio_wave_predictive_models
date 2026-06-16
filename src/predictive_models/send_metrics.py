import asyncio

from src.core.database import Session
from src.models import PredictiveModelsSchemaCreate, PredictiveModelsModel
from src.repositories import PredictiveModelsRepository


MIN_R2 = 0.1


async def __select_model_by_predictor(models):
    models_by_predictor = {}
    for predictor in models:
        valid = [m for m in models[predictor] if m is not None]
        if not valid:
            continue
        best_model = max(valid, key=lambda x: x['r2_mean'] - x['r2_std'])
        # print(best_model)
        if best_model['r2_mean'] - best_model['r2_std'] >= MIN_R2:
            models_by_predictor[predictor] = best_model
    return models_by_predictor


async def __select_models(group_result):
    tasks = []
    for result in group_result:
        tasks.append(asyncio.create_task(__select_model_by_predictor(result)))
    result = await asyncio.gather(*tasks)
    return result


def _build_instance(data, variable, group_id):
    params = data['coefficients'].copy()
    params['intercept'] = data['intercept']
    return PredictiveModelsModel(**PredictiveModelsSchemaCreate(**{
        "model": data['model'],
        "params": params,
        "predictable_variable": variable,
        "r2": data['r2_mean'],
        "mae": data['mae_log'],
        "rmse": data['rmse_log'],
        "residual_std": data['residual_std_log'],
        "group_id": group_id,
    }).model_dump())


def send_train_result_to_db(train_result):
    try:
        with Session() as session:
            predictive_models_repo = PredictiveModelsRepository(session)
            for result in train_result:
                model_data = asyncio.run(__select_models(result.values()))
                for data in model_data:
                    group_id = next(iter(result))

                    for variable in ('likes', 'comms', 'reposts'):
                        model = data.get(variable)
                        if model is not None:
                            instance = _build_instance(model, variable, group_id)
                            predictive_models_repo.add(instance)

            predictive_models_repo.commit()
    except Exception as e:
        raise
