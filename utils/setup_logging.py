
def setup_logging() -> None:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def setup_logging(
    logger: logging.Logger | None = None,
    logger_name: str | None = None,
    level: str = "DEBUG",
    clear: bool = True,
) -> logging.Logger:
    if logger is None and logger_name is None:
        raise ValueError("Provide either logger object or logger name")
    logger = logger or logging.getLogger(logger_name)
    handle = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s -- %(message)s"
    )
    handle.setFormatter(formatter)
    if clear:
        logger.handlers.clear()
    logger.addHandler(handle)
    logger.setLevel(level)
    return logger


def setup_logging() -> None:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def setup_logging(verbosity: int, no_color: bool, user_log_file: str | None) -> int:
    """Configures and sets up all of the logging

    Returns the requested logging level, as its integer value.
    """

    # Determine the level to be logging at.
    if verbosity >= 2:
        level_number = logging.DEBUG
    elif verbosity == 1:
        level_number = VERBOSE
    elif verbosity == -1:
        level_number = logging.WARNING
    elif verbosity == -2:
        level_number = logging.ERROR
    elif verbosity <= -3:
        level_number = logging.CRITICAL
    else:
        level_number = logging.INFO

    level = logging.getLevelName(level_number)

    # The "root" logger should match the "console" level *unless* we also need
    # to log to a user log file.
    include_user_log = user_log_file is not None
    if include_user_log:
        additional_log_file = user_log_file
        root_level = "DEBUG"
    else:
        additional_log_file = "/dev/null"
        root_level = level

    # Disable any logging besides WARNING unless we have DEBUG level logging
    # enabled for vendored libraries.
    vendored_log_level = "WARNING" if level in ["INFO", "ERROR"] else "DEBUG"

    # Shorthands for clarity
    handler_classes = {
        "stream": "pip._internal.utils.logging.RichPipStreamHandler",
        "file": "pip._internal.utils.logging.BetterRotatingFileHandler",
    }
    handlers = ["console", "console_errors", "console_subprocess"] + (
        ["user_log"] if include_user_log else []
    )
    global _stdout_console, stderr_console
    _stdout_console = PipConsole(file=sys.stdout, no_color=no_color, soft_wrap=True)
    _stderr_console = PipConsole(file=sys.stderr, no_color=no_color, soft_wrap=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "exclude_warnings": {
                    "()": "pip._internal.utils.logging.MaxLevelFilter",
                    "level": logging.WARNING,
                },
                "restrict_to_subprocess": {
                    "()": "logging.Filter",
                    "name": subprocess_logger.name,
                },
                "exclude_subprocess": {
                    "()": "pip._internal.utils.logging.ExcludeLoggerFilter",
                    "name": subprocess_logger.name,
                },
            },
            "formatters": {
                "indent": {
                    "()": IndentingFormatter,
                    "format": "%(message)s",
                },
                "indent_with_timestamp": {
                    "()": IndentingFormatter,
                    "format": "%(message)s",
                    "add_timestamp": True,
                },
            },
            "handlers": {
                "console": {
                    "level": level,
                    "class": handler_classes["stream"],
                    "console": _stdout_console,
                    "filters": ["exclude_subprocess", "exclude_warnings"],
                    "formatter": "indent",
                },
                "console_errors": {
                    "level": "WARNING",
                    "class": handler_classes["stream"],
                    "console": _stderr_console,
                    "filters": ["exclude_subprocess"],
                    "formatter": "indent",
                },
                # A handler responsible for logging to the console messages
                # from the "subprocessor" logger.
                "console_subprocess": {
                    "level": level,
                    "class": handler_classes["stream"],
                    "console": _stderr_console,
                    "filters": ["restrict_to_subprocess"],
                    "formatter": "indent",
                },
                "user_log": {
                    "level": "DEBUG",
                    "class": handler_classes["file"],
                    "filename": additional_log_file,
                    "encoding": "utf-8",
                    "delay": True,
                    "formatter": "indent_with_timestamp",
                },
            },
            "root": {
                "level": root_level,
                "handlers": handlers,
            },
            "loggers": {"pip._vendor": {"level": vendored_log_level}},
        }
    )

    return level_number


def setup_logging():
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter(
      "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  root.addHandler(handler)


def setup_logging() -> None:
    env = os.environ.get("OPENAI_LOG")
    if env == "debug":
        _basic_config()
        logger.setLevel(logging.DEBUG)
        httpx_logger.setLevel(logging.DEBUG)
    elif env == "info":
        _basic_config()
        logger.setLevel(logging.INFO)
        httpx_logger.setLevel(logging.INFO)


def setup_logging(verbose):
    log_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        log_handler.setFormatter(logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s"))
        logging_level = logging.DEBUG
    else:
        log_handler.setFormatter(logging.Formatter("%(filename)20s: %(message)s"))
        logging_level = logging.INFO
    log_handler.setLevel(logging_level)
    logger.addHandler(log_handler)
    logger.setLevel(logging_level)

