import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    PREDICTION_FILES_DIRECTORY: str = os.getenv(
        "PREDICTION_FILES_DIRECTORY", "prediction_files")
    PREDICTION_TRACKING_FILE: str = "prediction_tracking.json"
    PREDICTION_DONE: str = "done"
    PREDICTION_PROCESSING: str = "processing"
    MINIMUM_NUM_PRICE_HISTORY: int = 23
    NUM_REQUESTS_TO_PROCESS: int = 1
    LOGGER_NAME: str = os.getenv("LOGGER_NAME", "prediction-logging")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG").upper()

    BENCHMARK_RECORDS_DIRECTORY: str = os.getenv(
        "BENCHMARK_RECORDS_DIRECTORY", "benchmark_records")
    BENCHMARK_TRACKING_JSON: str = os.getenv(
        "BENCHMARK_TRACKING_JSON", "benchmark_tracking.json")
    BENCHMARK_TEST_FILES_DIRECTORY: str = os.getenv(
        "BENCHMARK_TEST_FILES_DIRECTORY", "benchmark-test-files")
    STATS_DIRECTORY: str = os.getenv(
        "STATS_DIRECTORY", "stats_files")

    GPT_TEMPERATURE: float = float(os.getenv("GPT_TEMPERATURE", 0.5))
    GPT_TOP_P: float = float(os.getenv("GPT_TOP_P", 1.0))

    CHAR_PER_PREDICTION: int = 2

    CELERY_PREDICTION_WORKER_NAME: str = os.getenv(
        "CELERY_PREDICTION_WORKER_NAME", "prediction_worker")
    CELERY_BACKEND: str = os.getenv(
        "CELERY_BACKEND", "redis://redis:6379/0")
    CELERY_BROKER: str = os.getenv(
        "CELERY_BROKER", "redis://redis:6379/0")
