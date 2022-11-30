from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    env_state: str

    class Config:
        env_file = ".env"


settings = Settings()
