from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    elasticsearch_url: str
    cassandra_hosts: list[str]

    class Config:
        env_file = ".env"
