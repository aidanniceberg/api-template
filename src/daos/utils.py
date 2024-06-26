from functools import wraps
from logging import Logger

from sqlalchemy.exc import OperationalError


def errorhandle(logger: Logger):
    def decorator(func: callable):
        @wraps(func)
        def error_handler(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except OperationalError as e:
                logger.error(f"Connection error in {func.__name__}: {e}")
                raise
            except Exception as e:
                logger.error(
                    f"An unexpected exception occurred in {func.__name__}: {e}"
                )
                raise

        return error_handler

    return decorator
