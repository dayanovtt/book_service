from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
    )


    @property
    def database_url(self) -> str:
        auth = self.postgres_user
        if self.postgres_password:
            auth += f":{self.postgres_password}"

        return (
            f"postgresql+psycopg2://"
            f"{auth}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

settings = Settings()
