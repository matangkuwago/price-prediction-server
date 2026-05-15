from celery import Celery
from celery.utils.log import get_task_logger
from typing import Union
from app.config import Config
from app.schemas import PredictionInput, Predictions, PredictionError
from app.celery.prediction import predict, get_checkpoints


# Configure Celery to use Redis as the message broker
celery_app = Celery(
    Config.CELERY_PREDICTION_WORKER_NAME,
    broker=Config.CELERY_BROKER,
    backend=Config.CELERY_BACKEND,
)


@celery_app.task
def run_prediction(prediction_input_params):
    prediction_input = PredictionInput.model_validate(prediction_input_params)

    if prediction_input.model not in get_checkpoints():
        error_message = f"Invalid model: {prediction_input.model}"
        return {
            'prediction_input': prediction_input_params,
            'error_message': error_message
        }
    try:
        predictions = predict(prediction_input)
    except Exception as e:
        logger = get_task_logger(__name__)
        logger.error(f"Task failed: {e}", exc_info=True)
        error_message = f"Prediction failed due to an internal system error."
        return {
            'prediction_input': prediction_input_params,
            'error_message': error_message
        }
    return predictions


@celery_app.task
def get_models():
    models = get_checkpoints()
    return models
