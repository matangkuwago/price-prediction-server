from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app


client = TestClient(app)


def test_result_not_yet_available():

    with patch('app.routers.results.AsyncResult') as mock_async_result:
        expected_status_code = status.HTTP_418_IM_A_TEAPOT
        mock_request_id = "68f4e1ed-77fb-4453-81b1-f3ba5b54d7d1"
        mock_result = Mock(ready=lambda: False)
        mock_async_result.return_value = mock_result

        response = client.get(f"/results/{mock_request_id}")
        assert response.status_code == expected_status_code


def test_result_available():

    with patch('app.routers.results.AsyncResult') as mock_async_result:
        expected_status_code = status.HTTP_200_OK
        mock_prediction_result = {
            "predictions": ["up", "down"],
            "error_message": None
        }
        mock_request_id = "68f4e1ed-77fb-4453-81b1-f3ba5b54d7d1"
        mock_result = Mock(ready=lambda: True,
                           get=lambda: mock_prediction_result)
        mock_async_result.return_value = mock_result

        response = client.get(f"/results/{mock_request_id}")
        assert response.status_code == expected_status_code


def test_result_available_prediction_error():

    with patch('app.routers.results.AsyncResult') as mock_async_result:
        expected_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        mock_prediction_result = {
            "predictions": [],
            "error_message": "Invalid model"
        }
        mock_request_id = "68f4e1ed-77fb-4453-81b1-f3ba5b54d7d1"
        mock_result = Mock(ready=lambda: True,
                           get=lambda: mock_prediction_result)
        mock_async_result.return_value = mock_result

        response = client.get(f"/results/{mock_request_id}")
        assert response.status_code == expected_status_code
