import logging

def is_logging_enabled(logger: logging.Logger) -> bool:
    """
    Checks if debug logging is enabled for the given logger.

    Args:
        logger: The logging.Logger instance to check.

    Returns:
        True if debug logging is enabled, False otherwise.
    """
    # NOTE: Log propagation to the root logger is disabled unless
    # the base logger i.e. logging.getLogger("google") is
    # explicitly configured by the end user. Ideally this
    # needs to happen in the client layer (already does for GAPICs).
    # However, this is implemented here to avoid logging
    # (if a root logger is configured) when a version of google-auth
    # which supports logging is used with:
    #  - an older version of a GAPIC which does not support logging.
    #  - Apiary client which does not support logging.
    global _LOGGING_INITIALIZED
    if not _LOGGING_INITIALIZED:
        base_logger = logging.getLogger(_BASE_LOGGER_NAME)
        if not _logger_configured(base_logger):
            base_logger.propagate = False
        _LOGGING_INITIALIZED = True

    return logger.isEnabledFor(logging.DEBUG)

