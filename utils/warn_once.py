import logging

def warn_once(logger_instance: logging.Logger, msg: str) -> None:
    """Log a warning message only once per unique message.

    Uses a global set to track messages that have already been logged
    to prevent duplicate warning messages from cluttering the output.

    Args:
        logger_instance: The logger instance to use for warning.
        msg: The warning message to log.
    """
    if msg not in _warn_once_logged:
        logger_instance.warning(msg)
        _warn_once_logged.add(msg)


def warn_once(msg: str, stacklevel: int = 1) -> None:
    # Dynamo causes all warnings.warn (in user code and in Dynamo code) to print all the time.
    # https://github.com/pytorch/pytorch/issues/128427.
    # warn_once is a workaround: if the msg has been warned on before, then we will not
    # warn again.
    # NB: it's totally ok to store a cache of all the strings: this is what warnings.warn does as well.
    if msg in warn_once_cache:
        return
    warn_once_cache.add(msg)
    warnings.warn(msg, stacklevel=stacklevel + 1)

