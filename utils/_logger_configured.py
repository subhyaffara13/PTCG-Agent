import logging

def _logger_configured(logger: logging.Logger) -> bool:
    """Determines whether `logger` has non-default configuration

    Args:
      logger: The logger to check.

    Returns:
      bool: Whether the logger has any non-default configuration.
    """
    return (
        logger.handlers != [] or logger.level != logging.NOTSET or not logger.propagate
    )

