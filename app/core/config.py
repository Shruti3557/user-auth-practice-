from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str= "HS256"
    access_token_expire_minutes: int= 15
    refresh_token_expire_days: int = 7
    otp_expire_minutes: int= 5
    otp_length: int= 6

    class Config:
        env_file= ".env"

settings= Settings()