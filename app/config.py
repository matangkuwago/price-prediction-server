from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):

    GPT_TEMPERATURE: float = 0.5
    GPT_TOP_P: float = 0

    CHAR_PER_PREDICTION: int = 2

    CELERY_PREDICTION_WORKER_NAME: str = "prediction_worker"
    CELERY_BACKEND: str = "redis://redis:6379/0"
    CELERY_BROKER: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


Config = ConfigSettings()
