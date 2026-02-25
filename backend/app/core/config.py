from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_TOKEN: str
    OPENAI_API_BASE: str
    OPENAI_API_KEY: str
    MODEL_NAME: str


settings = Settings()
