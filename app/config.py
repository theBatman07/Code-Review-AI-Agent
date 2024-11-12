from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    github_token: str
    ollama_url: str = "http://127.0.0.1:11434"
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str

    class Config:
        env_file = ".env"

settings = Settings()