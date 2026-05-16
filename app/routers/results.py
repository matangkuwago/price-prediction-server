from fastapi import APIRouter, HTTPException, status
from app.schemas import Predictions, ResponseMessage
from celery.result import AsyncResult
from app.celery.celery_worker import celery_app

router = APIRouter()


@router.get('/{request_id}', responses={
    status.HTTP_200_OK: {"model": Predictions},
    status.HTTP_418_IM_A_TEAPOT: {"model": ResponseMessage,
                                  "description": "Result is not yet available"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMessage,
                                            "description": "Prediction failed due to an internal system error."},
})
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
        if prediction_result["error_message"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=prediction_result["error_message"]
            )
        else:
            return Predictions(predictions=prediction_result["predictions"])
