from typing import Protocol
from ..domain.models import PredictionInput, PredictionResult

class PredictionStrategy(Protocol):
    """Interface for prediction strategies"""
    
    def predict(self, input_data: PredictionInput) -> PredictionResult:
        """Predict the outcome"""
        ... 
