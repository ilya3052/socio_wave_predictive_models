import asyncio

from src.core.database import Session
from src.models import PredictiveModelsSchemaCreate, PredictiveModelsModel
from src.repositories import PredictiveModelsRepository


async def __select_model_by_predictor(models):
    models_by_predictor = {}
    for predictor in models:
        best_model = max(models[predictor], key=lambda x: x['r2_mean'] - x['r2_std'])
        models_by_predictor[predictor] = best_model
    return models_by_predictor


async def __select_models(group_result):
    tasks = []
    for result in group_result:
        tasks.append(asyncio.create_task(__select_model_by_predictor(result)))
    result = await asyncio.gather(*tasks)
    return result


def prepare_model_coef(model_data):
    likes = model_data.get('likes')
    likes_params = likes.get('coefficients')
    likes_params['intercept'] = likes.get('intercept')

    comms = model_data.get('comms')
    comms_params = comms.get('coefficients')
    comms_params['intercept'] = comms.get('intercept')

    reposts = model_data.get('reposts')
    reposts_params = reposts.get('coefficients')
    reposts_params['intercept'] = reposts.get('intercept')

    return likes_params, comms_params, reposts_params


def send_train_result_to_db(train_result):
    try:
        with Session() as session:
            predictive_models_repo = PredictiveModelsRepository(session)
            for result in train_result:  # type: dict
                model_data = asyncio.run(__select_models(result.values()))
                for data in model_data:
                    likes_data = data.get('likes')
                    comms_data = data.get('comms')
                    reposts_data = data.get('reposts')

                    likes, comms, reposts = prepare_model_coef(data)
                    # ic(likes, comms, reposts)
                    group_id = next(iter(result))
                    predictive_models_list = predictive_models_repo.get_by_group_id(group_id)
                    if predictive_models_list:
                        pass

                    predictive_models_likes_schema = PredictiveModelsSchemaCreate(**{
                        "model": likes_data.get('model'),
                        "params": likes,
                        "predictable_variable": "likes",
                        "r2": likes_data.get('r2_mean'),
                        "mae": likes_data.get('mae_log'),
                        "rmse": likes_data.get('rmse_log'),
                        "residual_std": likes_data.get('residual_std_log'),
                        "group_id": group_id,
                    })
                    predictive_models_likes_instance = PredictiveModelsModel(
                        **predictive_models_likes_schema.model_dump())

                    predictive_models_comms_schema = PredictiveModelsSchemaCreate(**{
                        "model": comms_data.get('model'),
                        "params": comms,
                        "predictable_variable": "comms",
                        "r2": comms_data.get('r2_mean'),
                        "mae": comms_data.get('mae_log'),
                        "rmse": comms_data.get('rmse_log'),
                        "residual_std": comms_data.get('residual_std_log'),
                        "group_id": group_id,
                    })

                    predictive_models_comms_instance = PredictiveModelsModel(
                        **predictive_models_comms_schema.model_dump())

                    predictive_models_reposts_schema = PredictiveModelsSchemaCreate(**{
                        "model": reposts_data.get('model'),
                        "params": reposts,
                        "predictable_variable": "reposts",
                        "r2": reposts_data.get('r2_mean'),
                        "mae": reposts_data.get('mae_log'),
                        "rmse": reposts_data.get('rmse_log'),
                        "residual_std": reposts_data.get('residual_std_log'),
                        "group_id": group_id,
                    })

                    predictive_models_reposts_instance = PredictiveModelsModel(
                        **predictive_models_reposts_schema.model_dump())

                    predictive_models_repo.add(predictive_models_likes_instance)
                    predictive_models_repo.add(predictive_models_comms_instance)
                    predictive_models_repo.add(predictive_models_reposts_instance)

            predictive_models_repo.commit()
    except Exception as e:
        raise
