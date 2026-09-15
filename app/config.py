from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    cors_origins: list[str]
    gemini_api_key: str
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )
    
settings = Settings() # type: ignore (подтягивается в runtime из .env)