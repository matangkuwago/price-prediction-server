from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app


client = TestClient(app)


def test_get_available_models():
    with patch('app.routers.models.get_models') as mock_get_models:
        expected_status_code = 200
        available_models = ["model1", "model2", "model3"]
        mock_task = Mock(ready=lambda: True, result=available_models)
        mock_get_models.delay = lambda: mock_task

        response = client.get("/models")
        assert response.status_code == expected_status_code
        assert response.json() == {"models": available_models}
