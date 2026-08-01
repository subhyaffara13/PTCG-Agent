
def set_loglevel(level: LogLevel) -> None:
    return matplotlib.set_loglevel(level)


def set_loglevel(level):
    """
    Configure Matplotlib's logging levels.

    Matplotlib uses the standard library `logging` framework under the root
    logger 'matplotlib'.  This is a helper function to:

    - set Matplotlib's root logger level
    - set the root logger handler's level, creating the handler
      if it does not exist yet

    Typically, one should call ``set_loglevel("INFO")`` or
    ``set_loglevel("DEBUG")`` to get additional debugging information.

    Users or applications that are installing their own logging handlers
    may want to directly manipulate ``logging.getLogger('matplotlib')`` rather
    than use this function.

    Parameters
    ----------
    level : {"NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        The log level as defined in `Python logging levels
        <https://docs.python.org/3/library/logging.html#logging-levels>`__.

        For backwards compatibility, the levels are case-insensitive, but
        the capitalized version is preferred in analogy to `logging.Logger.setLevel`.

    Notes
    -----
    The first time this function is called, an additional handler is attached
    to Matplotlib's root handler; this handler is reused every time and this
    function simply manipulates the logger and handler's level.

    """
    _log.setLevel(level.upper())
    _ensure_handler().setLevel(level.upper())

