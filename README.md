# price-prediction-server

## About The Project
This is a price prediction API backend for Polymarket 5-minute markets. This repo uses GPT-2 Text-Generating models to predict up or down price movements. To train a GPT-2 model, you can use this [Google Colab notebook](https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce).

The backend has two endpoints:

| Method | Endpoint       | Description                  | Response Status Codes                  |
|--------|----------------|------------------------------|----------------------------------------|
| POST   | /predict       | Create a prediction request  | 202 (Accepted)                         |
| GET    | /get_results/{request_id}| Get prediction results | 418 if request is still in process, <br/>200 if the result is available |

### Create a prediction request
**Required Parameters:**
1. `ticker` - The ticker e.g. BTC for Bitcoin, ETH for Ethereum, etc.
2. `price_history` - Array of latest price history
3. `num_predictions` - Number of predictions needed

**Sample Code:**
```python
headers = {'Authorization': f'Bearer {auth_token}'}
data = {
    "ticker": "BTC",
    "price_history": [67100, 68100, 69100, 70100],
    "num_predictions": 5,
}
response = requests.post(f'{server}/predict', json=data, headers=headers)
```
**Sample Response:**
```python
{
  "request_id": "job_abc123_xyz"
}
```

### Get prediction results
**Required Parameters:**
1. `request_id` - The ```request_id``` returned by ```/predict```

**Sample Code:**
```python
headers = {'Authorization': f'Bearer {auth_token}'}
response = requests.get(f'{server}/get_results/{request_id}', headers=headers)
```
**Sample Response:**
```python
{
    "result": [
        "up",
        "down",
        "down",
        "down",
        "down"
    ]
}
```

## Installation and Usage

1. Create a python virtual environment, use the python version in the `.python-version` file and install the pip packages in the `requirements.txt` file.
2. Run ```./run_flask.sh``` to start the Flask server.
3. Run ```./prediction_loop.sh``` to start the prediction engine.
