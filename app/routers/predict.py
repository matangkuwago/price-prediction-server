from fastapi import APIRouter, HTTPException, status
from app.schemas import PredictionInput, Predictions, RequestResponse
from app.celery.celery_worker import run_prediction


router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED, response_model=RequestResponse)
async def create_prediction_request(prediction_input: PredictionInput):
    """
    Create a new prediction request
    """
    task_params = prediction_input.model_dump()
    task = run_prediction.delay(task_params)
    return {"request_id": task.id}
