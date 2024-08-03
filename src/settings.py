import dotenv
import os
from dataclasses import dataclass

dotenv.load_dotenv()


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
    environment: str

    @property
    def is_prod(self) -> bool:
        return self.environment == "production"


def get_settings():
    return Settings(
        db_config=DBConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            username=os.getenv("DB_USER", "template-user"),  # db username
            password=os.getenv("DB_PASSWORD", "template-password"),  # db password
            database=os.getenv("DB_NAME", "template-dbname"),  # db name
        ),
        environment=os.getenv("ENVIRONMENT", "development")
    )
