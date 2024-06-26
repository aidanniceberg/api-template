from dataclasses import dataclass


@dataclass
class DBConfig:
    username: str = ""
    password: str = ""
    host: str = "localhost"
    port: str = "5432"
    database: str = ""
    dialect: str = "postgresql"
    driver: str = "psycopg2"


@dataclass
class Settings:
    db_config: DBConfig


def get_settings():
    return Settings(
        db_config=DBConfig(
            username="template-user",  # db username
            password="template-password",  # db password
            database="template-dbname",  # db name
        )
    )
