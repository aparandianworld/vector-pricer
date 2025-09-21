from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str
    openai_base_url: str
    postgres_url: str = "sqlite:///data/laptops.db"
    vector_db_path: str = "faiss_index"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()