import unittest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.schemas import PredictionInput
from app.main import app


class TestEndpointPredict(unittest.TestCase):
    client = TestClient(app)

    def test_predict(self):
        expected_status_code = status.HTTP_202_ACCEPTED
        with patch('app.routers.predict.run_prediction') as mock_run_prediction:
            mock_task_id = "724c0383-d398-4658-a37a-29ed6c2ada6f"
            mock_task = Mock(id=mock_task_id)
            mock_run_prediction.delay = Mock(return_value=mock_task)
            # mock_run_prediction.delay = lambda x: mock_task
            post_params = {
                "model": "model1",
                "temperature": 0.5,
                "price_history": [1, 2, 3, 4, 5],
                "num_predictions": 1
            }
            response = self.client.post(
                "/predict",
                json=post_params,
            )

            prediction_input = PredictionInput(**post_params).model_dump()
            mock_run_prediction.delay.assert_called_with(prediction_input)
            assert response.status_code == expected_status_code
            assert response.json() == {"request_id": mock_task_id}

    def test_predict_invalid_price_history(self):
        expected_status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        with patch('app.routers.predict.run_prediction') as mock_run_prediction:
            mock_task_id = "49a37617-cf4b-4014-b92f-1c5f67288767"
            mock_task = Mock(id=mock_task_id)
            mock_run_prediction.delay = Mock(return_value=mock_task)
            post_params = {
                "model": "model1",
                "temperature": 0.5,
                "price_history": [],
                "num_predictions": 1
            }
            response = self.client.post(
                "/predict",
                json=post_params,
            )

            assert response.status_code == expected_status_code
            error_message = response.json()["detail"][0]["msg"]
            assert error_message == "List should have at least 2 items after validation, not 0"

    def test_predict_invalid_num_predictions(self):
        expected_status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        with patch('app.routers.predict.run_prediction') as mock_run_prediction:
            mock_task_id = "e8d2a472-ca12-4019-afed-83df886bc14a"
            mock_task = Mock(id=mock_task_id)
            mock_run_prediction.delay = Mock(return_value=mock_task)
            post_params = {
                "model": "model1",
                "temperature": 0.5,
                "price_history": [4, 5, 6, 7],
                "num_predictions": 0
            }
            response = self.client.post(
                "/predict",
                json=post_params,
            )

            assert response.status_code == expected_status_code
            error_message = response.json()["detail"][0]["msg"]
            assert error_message == "Input should be greater than 0"
