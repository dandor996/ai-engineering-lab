from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    sla_timeout_seconds: int = 10
    
    model_config = SettingsConfigDict(env_file='.env')
    