import jwt
from config.settings import Settings
import pytest
import main
import os
from fastapi.testclient import TestClient
from api.dependencies.services import get_prediction_orchestrator
from core.orchestrator.orchestrator import InferenceOrchestrator
from adapters.mock_predictor import MockPredictorA

os.environ["JWT_SECRET_KEY"] = "supersecretkey_per_i_test_minimo_32_chars"

settings = Settings()

@pytest.fixture
def client():
    return TestClient(main.app)

def test_inference_api(client: TestClient):
    token = jwt.encode({'user': 'test'}, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    response = client.post('/api/v1/predict', headers={'Authorization': f'Bearer {token}'}, json={'features': [1, 2, 3]})
    assert response.status_code == 200

def test_inference_api_missing_token(client: TestClient):
    response = client.post('/api/v1/predict', json={'features': [1, 2, 3]})
    assert response.status_code == 401

def test_inference_api_invalid_data(client: TestClient):
    token = jwt.encode({'user': 'test'}, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    response = client.post('/api/v1/predict', headers={'Authorization': f'Bearer {token}'}, json={'features': []})
    assert response.status_code == 422

def test_inference_api_timeout(client: TestClient):
    main.app.dependency_overrides[get_prediction_orchestrator] = lambda: InferenceOrchestrator(MockPredictorA(sleep_time=0.05), timeout=0.01)

    token = jwt.encode({'user': 'test'}, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    response = client.post('/api/v1/predict', headers={'Authorization': f'Bearer {token}'}, json={'features': [1, 2, 3]})
    assert response.status_code == 504
    main.app.dependency_overrides.clear()