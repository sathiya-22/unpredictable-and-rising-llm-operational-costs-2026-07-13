from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict, SecretStr

class Settings(BaseSettings):
    """
    Configuration settings for the LLM application.
    Loads values from environment variables or a .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="GEMINI_", # Expects env vars like GEMINI_API_KEY
    )

    api_key: SecretStr = Field(alias="API_KEY")
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: int = 500
    cost_per_token: float = 0.000002  # Added cost per token configuration
