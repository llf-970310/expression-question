from datetime import timedelta, datetime, timezone
import logging
import time
from functools import wraps


def func_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = 1000 * time.time()
        logging.info(f"=============  Begin: {func.__name__}  =============")
        logging.info(f"Args: {args}")
        try:
            rsp = func(*args, **kwargs)
            logging.info(f"Response: {rsp}")
            end = 1000 * time.time()
            logging.info(f"Time consuming: {end - start}ms")
            logging.info(f"=============   End: {func.__name__}   =============\n")
            return rsp
        except Exception as e:
            logging.error(repr(e))
            raise e

    return wrapper
