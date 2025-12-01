"""Configuration management using Pydantic Settings (dev-friendly)."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    API_KEY: Optional[str] = None

    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "mixtral-8x7b-32768"

    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_EMBED_MODEL: str = "models/text-embedding-004"

    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "contract-intelligence"

    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_PROJECT: str = "Contract-Intelligence-API"

    IP_RPM: int = 10
    IP_RPD: int = 500
    SESSION_RPM: int = 20
    SESSION_RPD: int = 1000

    DATABASE_URL: str = "postgresql://contract_user:contract_pass@postgres:5432/contracts_db"

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 4

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
