import logging
from typing import Any

def response_log(logger: logging.Logger, response: Any) -> None:
    """
    Logs an HTTP response at the DEBUG level if logging is enabled.

    Args:
        logger: The logging.Logger instance to use.
        response: The HTTP response object to log.
    """
    if is_logging_enabled(logger):
        json_response = _parse_response(response)
        _response_log_base(logger, json_response)

