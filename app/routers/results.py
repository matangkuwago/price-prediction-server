from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from app.schemas import Predictions
from celery.result import AsyncResult
from app.celery.celery_worker import celery_app

router = APIRouter()


@router.get('/{request_id}', response_model=Predictions)
async def get_prediction_results(request_id: str):

    res = AsyncResult(request_id, app=celery_app)

    if not res.ready():
        error_message = f"result for request_id {request_id} is not yet available"
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail=error_message
        )
    else:
        predictions = res.get()
        return {"predictions": predictions}
