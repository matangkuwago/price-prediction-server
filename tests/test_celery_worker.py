import unittest
from unittest.mock import patch
from pydantic import ValidationError
from app.celery.celery_worker import get_models, run_prediction


class TestGetModels(unittest.TestCase):
    """Tests for the get_models celery task."""

    @patch('app.celery.celery_worker.get_checkpoints')
    def test_get_models_returns_checkpoints(self, mock_get_checkpoints):
        """Test that get_models returns the list of checkpoints."""
        mock_get_checkpoints.return_value = ['model_1', 'model_2', 'model_3']

        result = get_models()

        self.assertEqual(result, ['model_1', 'model_2', 'model_3'])
        mock_get_checkpoints.assert_called_once()

    @patch('app.celery.celery_worker.get_checkpoints')
    def test_get_models_with_empty_checkpoints(self, mock_get_checkpoints):
        """Test get_models when there are no checkpoints."""
        mock_get_checkpoints.return_value = []

        result = get_models()

        self.assertEqual(result, [])


class TestRunPrediction(unittest.TestCase):
    """Tests for the run_prediction celery task."""

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_valid_model(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction with a valid model."""
        # Setup mocks
        mock_get_checkpoints.return_value = ['model_v1', 'model_v2']
        mock_predict.return_value = ['U-', 'S-', 'D-']

        # Valid prediction input parameters
        params = {
            'model': 'model_v1',
            'temperature': 0.7,
            'price_history': [100.0, 102.0, 101.0],
            'num_predictions': 1
        }

        result = run_prediction(params)

        # Validate response structure
        self.assertIn('predictions', result)
        self.assertIn('error_message', result)
        self.assertEqual(result['predictions'], ['U-', 'S-', 'D-'])
        self.assertIsNone(result['error_message'])
        mock_predict.assert_called_once()

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_invalid_model(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction with an invalid model."""
        # Setup mocks
        mock_get_checkpoints.return_value = ['model_v1']

        # Invalid model that's not in checkpoints
        params = {
            'model': 'nonexistent_model',
            'price_history': [100.0, 102.0],
            'num_predictions': 1
        }

        result = run_prediction(params)

        # Validate error response
        self.assertEqual(result['predictions'], [])
        self.assertIsNotNone(result['error_message'])
        self.assertIn('nonexistent_model', result['error_message'])
        mock_predict.assert_not_called()

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_model_in_checkpoints(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction when model exists in checkpoints."""
        # Setup mocks
        mock_get_checkpoints.return_value = ['model_v1']
        mock_predict.return_value = ['UP-', 'DOWN-']

        params = {
            'model': 'model_v1',
            'price_history': [100.0, 105.0, 100.0],
            'num_predictions': 1
        }

        result = run_prediction(params)

        self.assertEqual(result['predictions'], ['UP-', 'DOWN-'])
        self.assertIsNone(result['error_message'])

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_exception(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction when predict raises an exception."""
        # Setup mocks
        mock_get_checkpoints.return_value = ['model_v1']
        mock_predict.side_effect = Exception("Prediction failed")

        params = {
            'model': 'model_v1',
            'price_history': [100.0, 102.0],
            'num_predictions': 1
        }

        result = run_prediction(params)

        # Validate error response structure
        self.assertEqual(result['predictions'], [])
        self.assertIsNotNone(result['error_message'])
        self.assertEqual(
            result['error_message'], "Prediction failed due to an internal system error.")
        mock_predict.assert_called_once()

    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_missing_price_history(self, mock_get_checkpoints):
        """Test run_prediction when price_history is missing."""
        mock_get_checkpoints.return_value = ['model_v1']

        params = {
            'model': 'model_v1',
            'num_predictions': 1
        }

        # This should trigger validation error in PredictionInput
        with self.assertRaises(ValidationError):
            run_prediction(params)

    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_invalid_price_history_length(self, mock_get_checkpoints):
        """Test run_prediction with price_history shorter than required."""
        mock_get_checkpoints.return_value = ['model_v1']

        # Price history with only 1 element (minimum is 2)
        params = {
            'model': 'model_v1',
            'price_history': [100.0],
            'num_predictions': 1
        }

        with self.assertRaises(ValidationError):
            run_prediction(params)

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_zero_predictions(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction with num_predictions = 0."""
        mock_get_checkpoints.return_value = ['model_v1']
        mock_predict.return_value = []

        # num_predictions should be greater than 0
        params = {
            'model': 'model_v1',
            'price_history': [100.0, 102.0],
            'num_predictions': 0
        }

        with self.assertRaises(ValidationError):
            run_prediction(params)

    @patch('app.celery.celery_worker.predict')
    @patch('app.celery.celery_worker.get_checkpoints')
    def test_run_prediction_with_default_values(self, mock_get_checkpoints, mock_predict):
        """Test run_prediction with default values for temperature and top_p."""
        mock_get_checkpoints.return_value = ['model_v1']
        mock_predict.return_value = ['U-']

        params = {
            'model': 'model_v1',
            'price_history': [100.0, 102.0],
            # temperature and top_p should use defaults
            'num_predictions': 1
        }

        result = run_prediction(params)

        self.assertIn('predictions', result)
        self.assertIsNone(result['error_message'])
