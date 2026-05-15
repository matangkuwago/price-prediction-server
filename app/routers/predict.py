from fastapi import APIRouter, status
from app.schemas import (
    PredictionInput,
    CreatePredictionRequestResponse
)
from app.celery.celery_worker import run_prediction


router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED, response_model=CreatePredictionRequestResponse)
async def create_prediction_request(prediction_input: PredictionInput):
    task_params = prediction_input.model_dump()
    task = run_prediction.delay(task_params)
    return {"request_id": task.id}
