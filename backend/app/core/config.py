from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_TOKEN: str
    OPENAI_API_BASE: str
    OPENAI_API_KEY: str
    MODEL_NAME: str
    MODEL_TEMPERATURE: float = 0.2
    MODEL_TOP_P: float | None = None
    MODEL_EXTRA_BODY: str | None = None


settings = Settings()
