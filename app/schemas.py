from typing import Annotated
from annotated_types import Len
from datetime import datetime
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional, List


def get_timestamp():
    return int(datetime.now().timestamp())


class PredictionInput(BaseModel):
    model: str
    temperature: Optional[float] = 0.5
    price_history: Annotated[List[float], Len(min_length=2)]
    num_predictions: int = Field(gt=0)
    description: Optional[str] = None
    top_p: Optional[float] = 0
    _created_at: Optional[int] = PrivateAttr(default_factory=get_timestamp)


class ModelsResponse(BaseModel):
    models: List[str]


class CreatePredictionRequestResponse(BaseModel):
    request_id: str


class Predictions(BaseModel):
    predictions: List[str]
