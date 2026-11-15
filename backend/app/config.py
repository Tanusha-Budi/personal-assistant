from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Personal Assistant API"
    environment: str = "development"
    frontend_origin: str = "http://localhost:5173"
    anthropic_api_key: str = ""
    google_credentials_path: str = "secrets/google_credentials.json"
    google_token_path: str = "secrets/google_token.json"
    timezone: str = "Asia/Kolkata"
    github_token: str = ""
    llm_provider: str = "fake"            # "fake" or "anthropic"
    llm_model: str = "claude-haiku-5-5"
    llm_max_tokens: int = 1000
    agent_recursion_limit: int = 10
    log_level: str = "INFO"
    log_to_file: bool = True
    log_dir: str = "logs"


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()