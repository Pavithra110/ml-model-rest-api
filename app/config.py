from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_PATH: str = "ml/saved_model/model.joblib"
    LOG_LEVEL: str = "INFO"
    MAX_BATCH_SIZE: int = 100
    API_TITLE: str = "ML Model API"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()