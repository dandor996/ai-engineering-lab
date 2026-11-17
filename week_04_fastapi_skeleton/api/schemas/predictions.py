from pydantic import BaseModel
from typing import Self
from core.domain.models import PredictionInput, PredictionResult

class PredictionRequest(BaseModel):
    features: list[float]

    def to_domain(self) -> PredictionInput:
        return PredictionInput(features=self.features)

class PredictionResponse(BaseModel):
    score: float

    @classmethod
    def from_domain(cls, result: PredictionResult) -> Self:
        return cls(score=result.score)