import logging
from typing import Callable
from selenium.common.exceptions import TimeoutException
import traceback
youtube_logger = logging.getLogger('youtube_find.youtube_checker')


def error_handle(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException as e:
            # Log TimeoutException with a custom message
            youtube_logger.error(f'{func.__name__} element not found within the given time:\n {e}')
            return None
        except Exception as e:
            # Log all other exceptions with stack trace
            youtube_logger.exception(f'Error while retrieving {func.__name__}: {e}')
            # Log the stack trace to understand where the error happened
            youtube_logger.exception(f"Stack Trace: {traceback.format_exc()}")
            return None
    return wrapper