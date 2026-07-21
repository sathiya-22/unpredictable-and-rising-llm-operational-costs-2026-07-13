from pydantic import Field, model_validator
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

    @model_validator(mode='after')
    def validate_generation_parameters(self) -> 'Settings':
        """
        Validates the temperature and max_tokens settings.
        """
        if not (0.0 <= self.temperature <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0.")
        if not (1 <= self.max_tokens <= 8192): # Common range for Gemini models
            raise ValueError("Max tokens must be between 1 and 8192.")
        return self
