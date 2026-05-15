import asyncio
from fastapi import APIRouter, HTTPException, status
from app.schemas import ModelsResponse
from app.celery.celery_worker import get_models


router = APIRouter()


@router.get('/', response_model=ModelsResponse)
async def get_available_models():
    """
    Lists available models
    """
    task = get_models.delay()
    while not task.ready():
        await asyncio.sleep(0.1)
    return {"models": task.result}
