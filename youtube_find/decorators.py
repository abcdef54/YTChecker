import logging
from typing import Callable
from functools import wraps
from selenium.common.exceptions import TimeoutException
import traceback
youtube_logger = logging.getLogger('youtube_find.youtube_checker')


def error_handle(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException as e:
            # Log TimeoutException with a custom message
            youtube_logger.error(f'{func.__name__} - Element not found within the given time:\n {e}')
            return None
        except Exception as e:
            # Log all other exceptions with a stack trace
            youtube_logger.exception(f'Error in {func.__name__} with args={args}, kwargs={kwargs}: {e}')
            youtube_logger.exception(f"Stack Trace:\n{traceback.format_exc()}")
            raise
    return wrapper