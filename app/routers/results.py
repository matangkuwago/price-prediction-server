from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, status
from app.schemas import Predictions, PredictionError
from celery.result import AsyncResult
from app.celery.celery_worker import celery_app

router = APIRouter()


@router.get('/{request_id}', response_model=Union[Predictions, PredictionError])
async def get_prediction_results(request_id: str):

    res = AsyncResult(request_id, app=celery_app)

    if not res.ready():
        error_message = f"result for request_id {request_id} is not yet available"
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail=error_message
        )
    else:
        prediction_result = res.get()
        if isinstance(prediction_result, dict):
            return PredictionError(**prediction_result)
        else:
            return Predictions(predictions=prediction_result)
