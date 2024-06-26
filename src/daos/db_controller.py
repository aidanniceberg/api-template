import logging
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.settings import DBConfig, get_settings

logger = logging.getLogger(__name__)


class DBController:
    engine: Engine = None

    @staticmethod
    def _generate_connection_string(cfg: DBConfig) -> str:
        return (
            f"{cfg.dialect}+{cfg.driver}"
            f"://{cfg.username}:{cfg.password}"
            f"@{cfg.host}:{cfg.port}/{cfg.database}"
        )

    @classmethod
    def is_setup(cls):
        return cls.engine is not None

    @classmethod
    def setup(cls):
        if not cls.is_setup():
            config = get_settings().db_config
            connection_string = cls._generate_connection_string(cfg=config)
            cls.engine = create_engine(connection_string, pool_pre_ping=True)
        else:
            logger.warning("DBController already set up")

    @classmethod
    @contextmanager
    def session(cls):
        """
        Context manager that creates a new database session and closes it on teardown
        :return: session
        """
        if not cls.is_setup():
            cls.setup()
        session = None
        try:
            session = Session(cls.engine)
            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        finally:
            if session:
                session.close()
