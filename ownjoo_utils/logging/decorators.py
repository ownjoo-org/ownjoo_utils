import logging
from datetime import datetime, timedelta, timezone
from typing import Generator, Optional, AsyncGenerator

from ownjoo_utils.logging.consts import LOG_FORMAT
from ownjoo_utils.parsing.consts import TimeFormats


def timed_generator(
        log_progress: bool = True,
        log_progress_label: Optional[str] = None,
        log_progress_interval: int = 10000,
        log_level: int = logging.INFO,
        logger: Optional[logging.Logger] = None,
):
    if not isinstance(logger, logging.Logger):
        logging.basicConfig(
            format=LOG_FORMAT,
            level=logging.INFO,
            datefmt=TimeFormats.date_and_time.value,
        )
        logger = logging.getLogger(__name__)

    def decorator(func):
        def wrapper(*args, **kwargs) -> Generator:
            nonlocal log_progress_label
            if not log_progress_label:
                log_progress_label = func.__name__
            count: int = 0
            start = datetime.now(timezone.utc)
            if log_progress:
                logger.log(log_level, f'Started {log_progress_label} at {start.isoformat()}')
            for each in func(*args, **kwargs):
                yield each
                count += 1
                if log_progress:
                    if not count % log_progress_interval:
                        logger.log(log_level, f'Fetched {count} {log_progress_label} so far')
            end = datetime.now(timezone.utc)
            elapsed: timedelta = end - start
            if log_progress:
                logger.log(log_level, f'Ended {log_progress_label} at {end.isoformat()}')
            logger.log(log_level, f'Yielded {count} {log_progress_label} in {elapsed}')
        return wrapper
    return decorator


def timed_async_generator(
        log_progress: bool = True,
        log_progress_label: Optional[str] = None,
        log_progress_interval: int = 10000,
        log_level: int = logging.INFO,
        logger: Optional[logging.Logger] = None,
):
    if not isinstance(logger, logging.Logger):
        logging.basicConfig(
            format=LOG_FORMAT,
            level=logging.INFO,
            datefmt=TimeFormats.date_and_time.value,
        )
        logger = logging.getLogger(__name__)

    def decorator(func):
        async def wrapper(*args, **kwargs) -> AsyncGenerator:
            nonlocal log_progress_label
            if not log_progress_label:
                log_progress_label = func.__name__
            count: int = 0
            start = datetime.now(timezone.utc)
            if log_progress:
                logger.log(log_level, f'Started {log_progress_label} at {start.isoformat()}')
            async for each in func(*args, **kwargs):
                yield each
                count += 1
                if log_progress:
                    if not count % log_progress_interval:
                        logger.log(log_level, f'Fetched {count} {log_progress_label} so far')
            end = datetime.now(timezone.utc)
            elapsed: timedelta = end - start
            if log_progress:
                logger.log(log_level, f'Ended {log_progress_label} at {end.isoformat()}')
            logger.log(log_level, f'Yielded {count} {log_progress_label} in {elapsed}')
        return wrapper
    return decorator
