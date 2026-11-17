import pytest
from core.domain.exceptions import InvalidFeatureError, InvalidPredictionError, PredictionTimeoutError
from core.domain.models import PredictionInput, PredictionResult
from adapters.mock_predictor import MockPredictorA

def test_raises_invalid_prediction_error():
    with pytest.raises(expected_exception=InvalidPredictionError) as e:
        PredictionResult(score=1.5)

def test_raises_invalid_feature_error():
    with pytest.raises(expected_exception=InvalidFeatureError) as e:
        PredictionInput(features=[])

def test_prediction_input_success():
    PredictionInput(features=[1, 2, 3])

def test_prediction_result_success():
    PredictionResult(score=0.5)

def test_mock_predictor_a_clamping():
    predictor = MockPredictorA()
    result = predictor.predict(input_data = PredictionInput([1, 2, 3])) 
    assert result == PredictionResult(1.0)

def test_mock_predictor_a_success():
    predictor = MockPredictorA()
    result = predictor.predict(input_data = PredictionInput([0.2, 0.4])) 
    assert result.score == pytest.approx(0.3)