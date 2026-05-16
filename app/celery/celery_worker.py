from celery import Celery
from celery.utils.log import get_task_logger
from app.config import Config
from app.schemas import PredictionInput
from app.celery.prediction import predict, get_checkpoints


# Configure Celery to use Redis as the message broker
celery_app = Celery(
    Config.CELERY_PREDICTION_WORKER_NAME,
    broker=Config.CELERY_BROKER,
    backend=Config.CELERY_BACKEND,
)


@celery_app.task
def get_models():
    models = get_checkpoints()
    return models


@celery_app.task
def run_prediction(prediction_input_params):

    prediction_input = PredictionInput.model_validate(prediction_input_params)
    if prediction_input.model not in get_checkpoints():
        return {
            'predictions': [],
            'error_message': f"Invalid model: {prediction_input.model}"
        }

    try:
        return {
            'predictions': predict(prediction_input),
            'error_message': None
        }
    except Exception as e:
        get_task_logger(__name__).error(f"Task failed: {e}", exc_info=True)
        return {
            'predictions': [],
            'error_message': "Prediction failed due to an internal system error."
        }
