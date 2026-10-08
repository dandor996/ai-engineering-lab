import asyncio
from ..strategy.protocol import PredictionStrategy
from ..domain.models import PredictionInput, PredictionResult
from ..domain.exceptions import PredictionTimeoutError

class InferenceOrchestrator:
    def __init__(self, strategy: PredictionStrategy, timeout: int = 10):
        self.strategy = strategy
        self.timeout = timeout
    
    async def process_inference(self, input_data: PredictionInput) -> PredictionResult:
        try:
            return await asyncio.wait_for(asyncio.to_thread(self.strategy.predict, input_data), timeout=self.timeout)
        except asyncio.TimeoutError as exc:
            raise PredictionTimeoutError(f"Prediction timed out after {self.timeout} seconds") from exc
            