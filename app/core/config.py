from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_title: str = "Restaurant API"
    api_version: str = "1.0.0"

    db_user: str = "restaurant"
    db_pass: str = "restaurant"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "restaurant"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}")

settings = Settings()