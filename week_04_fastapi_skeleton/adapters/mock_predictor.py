import time
from core.domain.models import PredictionInput, PredictionResult

class MockPredictorA:
    def __init__(self, sleep_time: float = 0.0):
        self.sleep_time = sleep_time

    def predict(self, input_data: PredictionInput) -> PredictionResult:
        time.sleep(self.sleep_time)

        feats = input_data.features
        mean_val = sum(feats) / len(feats) if feats else 0.0
        score = max(0.0, min(mean_val, 1))
        return PredictionResult(score)

        