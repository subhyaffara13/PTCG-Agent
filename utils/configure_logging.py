
def configure_logging(
    verbosity: int,
    filename: str | None = None,
    logformat: str = LOG_FORMAT,
) -> None:
    """Configure logging for flake8.

    :param verbosity:
        How verbose to be in logging information.
    :param filename:
        Name of the file to append log information to.
        If ``None`` this will log to ``sys.stderr``.
        If the name is "stdout" or "stderr" this will log to the appropriate
        stream.
    """
    if verbosity <= 0:
        return

    verbosity = min(verbosity, max(_VERBOSITY_TO_LOG_LEVEL))
    log_level = _VERBOSITY_TO_LOG_LEVEL[verbosity]

    if not filename or filename in ("stderr", "stdout"):
        fileobj = getattr(sys, filename or "stderr")
        handler_cls: type[logging.Handler] = logging.StreamHandler
    else:
        fileobj = filename
        handler_cls = logging.FileHandler

    handler = handler_cls(fileobj)
    handler.setFormatter(logging.Formatter(logformat))
    LOG.addHandler(handler)
    LOG.setLevel(log_level)
    LOG.debug(
        "Added a %s logging handler to logger root at %s", filename, __name__
    )

