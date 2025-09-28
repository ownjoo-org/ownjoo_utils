import logging
from datetime import datetime
from typing import Any, Callable, Optional, Type, Union, Iterable

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


def validate(
        v: Any,
        exp: Type = None,
        default: Any = None,
        converter: Callable = None,
        validator: Optional[Callable] = DEFAULT_VALIDATOR,
        **kwargs
) -> Any:
    """
    generic validation utility
    :param v: Any: the value to be validated
    :param exp: Type: the expected type of the value
    :param default: Any: the default value to return if value is None
    :param converter: Callable: a function to convert the value to the desired result
    :param validator: Callable: a function to test that the result matches desired values
    :param kwargs: everything else is passed as **kwargs to converter and validator
    :return: Any: One of [the converted, validated value] | [the default value if specified, or None]
    """
    result: Any = v
    is_valid_result: bool = False

    # check pre-defined converters
    if not isinstance(converter, Callable):
        if exp is list:
            converter = str_to_list
        elif exp is datetime:
            converter = get_datetime
        else:
            converter = DEFAULT_CONVERTER  # pass through

    # convert values as needed
    try:
        result = converter(v, exp, **kwargs)
    except Exception as exc_str:
        logger.exception(f'Failed to parse {v=} with converter {converter}: {exc_str}')

    # check validator
    if not validator:
        validator = DEFAULT_VALIDATOR

    try:
        is_valid_result = validator(result, exp, **kwargs)
    except Exception as exc_validation:
        logger.exception(f'Failed validation: {validator=}: {exc_validation=}')

    if is_valid_result:
        return result
    else:
        return default


def get_value(
        src: Union[dict, Iterable],
        path: Union[None, int, list, str] = None,
        post_processor: Callable = validate,
        **kwargs
) -> Optional[Any]:
    """
    Return a validated value from a data structure if path is specified.  If not path is specified, the value will be
    post-processed by post_processor() with any kwargs specified.
    :param src: list or dict to recurse through according to path.  If not path this is treated as a single value to
     post_process().
    :param path: list[float, int, str]: list of values to use as dict key or list index to dive deeper into the struct.
    :param post_processor: Callable: any callable to perform any action on the found value.  Default: validate().
    :param kwargs: dict: any values to be passed to validate() (and it's converter and validator functions if specified)
    :return: Any: validated value from the nested src
    """
    keydex: Union[None, float, int, str] = path.pop(0) if path and isinstance(path, list) else None
    result = src[keydex] if keydex is not None else src
    if path and isinstance(result, (dict, list)):  # keep digging if needed
        return get_value(src=result, path=path, **kwargs)
    elif isinstance(post_processor, Callable):  # call the post-processor if needed
        return post_processor(result, **kwargs)
    else:
        return result  # return found value without post-processing
