from dataclasses import dataclass
from .exceptions import InvalidPredictionError, InvalidFeatureError

@dataclass
class PredictionInput:
    features: list[float]

    def __post_init__(self):
        if len(self.features) == 0:
            raise InvalidFeatureError("Feature list cannot be empty")

@dataclass
class PredictionResult:
    score: float
    
    def __post_init__(self):
        if self.score < 0 or self.score > 1:
            raise InvalidPredictionError("Prediction score must be between 0 and 1")
