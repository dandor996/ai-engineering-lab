from core.orchestrator.orchestrator import InferenceOrchestrator
from adapters.mock_predictor import MockPredictorA
from config.settings import Settings

def get_prediction_orchestrator() -> InferenceOrchestrator:
    settings = Settings()
    predictor = MockPredictorA()
    return InferenceOrchestrator(predictor, settings.sla_timeout_seconds)
    