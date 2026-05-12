from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


def get_timestamp():
    return int(datetime.now().timestamp())


class PredictionInput(BaseModel):
    model: str
    temperature: Optional[float] = 0.5
    price_history: List[float]
    num_predictions: int
    description: Optional[str] = None
    top_p: Optional[float] = 0
    created_at: Optional[int] = Field(default_factory=get_timestamp)


class Predictions(BaseModel):
    predictions: List[str]
