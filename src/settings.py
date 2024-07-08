import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    username: str = ""
    password: str = ""
    host: str = "localhost"
    port: int = 5432
    database: str = ""
    dialect: str = "postgresql"
    driver: str = "psycopg2"


@dataclass
class Settings:
    db_config: DBConfig


def get_settings():
    return Settings(
        db_config=DBConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            username="template-user",  # db username
            password="template-password",  # db password
            database="template-dbname",  # db name
        ),
    )
