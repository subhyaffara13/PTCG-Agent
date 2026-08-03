import logging
from typing import Any

def _response_log_base(logger: logging.Logger, parsed_response: Any) -> None:
    """
    Logs a parsed HTTP response at the DEBUG level.

    This internal helper function takes a parsed response and logs it
    using the provided logger. It also applies a hashing function to
    potentially sensitive information before logging.

    Args:
        logger: The logging.Logger instance to use for logging.
        parsed_response: The parsed HTTP response object (e.g., a dictionary,
            list, or the original response if parsing failed).
    """

    logged_response = _hash_sensitive_info(parsed_response)
    logger.debug("Response received...", extra={"httpResponse": logged_response})

