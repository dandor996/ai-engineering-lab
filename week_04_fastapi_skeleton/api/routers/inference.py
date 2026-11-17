from fastapi import Depends, APIRouter
from api.dependencies.auth import verify_token
from api.dependencies.services import get_prediction_orchestrator
from api.schemas.predictions import PredictionRequest, PredictionResponse
from core.orchestrator.orchestrator import InferenceOrchestrator

router = APIRouter()

@router.post("/predict", dependencies=[Depends(verify_token)], response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    orchestrator: InferenceOrchestrator = Depends(get_prediction_orchestrator)) -> PredictionResponse:

    model_input = request.to_domain()
    result = await orchestrator.process_inference(model_input)

    return PredictionResponse.from_domain(result)
