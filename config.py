from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # This tells Pydantic v2 to look for the .env file in the root directory
    model_config = SettingsConfigDict(env_file=".env")

# Instantiate it immediately so other files can import this single object
settings = Settings()