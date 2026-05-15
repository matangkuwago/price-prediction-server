from celery import Celery
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
def run_prediction(prediction_input_params):
    prediction_input = PredictionInput.model_validate(prediction_input_params)
    predictions = predict(prediction_input)
    return predictions


@celery_app.task
def get_models():
    models = get_checkpoints()
    return models
