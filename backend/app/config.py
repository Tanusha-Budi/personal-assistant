from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Personal Assistant API"
    environment: str = "development"
    frontend_origin: str = "http://localhost:5173"
    anthropic_api_key: str = ""
    google_credentials_path: str = "secrets/google_credentials.json"
    google_token_path: str = "secrets/google_token.json"
    timezone: str = "Asia/Kolkata"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()