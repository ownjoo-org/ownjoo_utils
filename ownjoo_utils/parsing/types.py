import logging
from datetime import datetime
from typing import Any, Callable, Optional, Type, Union

from ownjoo_utils.logging.consts import LOG_FORMAT
from ownjoo_utils.parsing.consts import DEFAULT_SEPARATOR, DEFAULT_VALIDATOR, TimeFormats, DEFAULT_CONVERTER

logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    datefmt=TimeFormats.date_and_time.value,
)
logger = logging.getLogger(__name__)


def str_to_list(v: Optional[str] = None, separator: str = DEFAULT_SEPARATOR, **kwargs) -> Optional[list[str]]:
    if not isinstance(v, str):
        return v
    if not isinstance(separator, str):
        separator = DEFAULT_SEPARATOR
    return v.split(separator)


def get_datetime(
        v: Union[None, datetime, float, str] = None,
        *args,
        format_str: Optional[str] = None,
        **kwargs
) -> Optional[datetime]:
    result: Optional[datetime] = v
    _last_result: Optional[datetime] = None
    if v is None:
        pass
    elif isinstance(v, (float, int)):  # if number treat as a timestamp (seconds from epoch)
        try:
            result = datetime.fromtimestamp(v)
            if not _last_result:
                _last_result = result
            elif _last_result != result:
                raise ValueError(f'Found conflicting timestamp: previous: {_last_result}, current: {result}')
        except Exception as exc_num:
            logger.exception(f'Failed to parse {v=} as timestamp: {exc_num}')
    elif isinstance(format_str, str):
        try:
            result = datetime.strptime(v, format_str)
        except Exception as exc_str:
            logger.exception(f'Failed to parse {v=} as {format_str}: {exc_str}')
    elif isinstance(v, str):
        for time_format in TimeFormats:  # if str try to parse the str from a known format
            try:
                result = datetime.strptime(v, time_format.value)
                if not _last_result:
                    _last_result = result
                elif _last_result != result:
                    raise ValueError(f'Found conflicting timestamp: previous: {_last_result}, current: {result}')
                break
            except Exception as exc_str:
                logger.exception(f'Failed to parse {v=} as {time_format.value} ({time_format}): {exc_str}')
    return result


def exp_type(
        v: Any,
        exp: Type = None,
        default: Any = None,
        converter: Callable = None,
        validator: Optional[Callable] = DEFAULT_VALIDATOR,
        separator: Optional[str] = None,
        **kwargs
) -> Any:
    result: Any = v
    is_valid_result: bool = False

    # check pre-defined converters
    if not isinstance(converter, Callable):
        if exp is list:
            converter = str_to_list
        elif exp is datetime:
            converter = get_datetime
        else:
            converter = DEFAULT_CONVERTER  # type cast

    # convert values as needed
    try:
        result = converter(v, exp=exp, converter=converter, validator=validator, separator=separator, **kwargs)
    except Exception as exc_str:
        logger.exception(f'Failed to parse {v=} with converter {converter}: {exc_str}')

    # check validator
    if not validator:
        validator = DEFAULT_VALIDATOR

    try:
        is_valid_result = validator(result, exp)
    except Exception as exc_validation:
        logger.exception(f'Failed validation: {validator=}: {exc_validation=}')

    if is_valid_result:
        return result
    else:
        return default
