from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_uri: str = 'sqlite:///animals.db'


settings = Settings()
