
def _init_logger():
    logger = logging.getLogger(__name__)

    level = os.environ.get("PYTORCH_MATCHER_LOGLEVEL", "WARNING").upper()
    logger.setLevel(level)
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(filename)s > %(message)s")
    console.setFormatter(formatter)
    console.setLevel(level)
    # add the handlers to the logger
    logger.addHandler(console)
    logger.propagate = False
    return logger


def _init_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)

    level = os.environ.get("PYTORCH_MATCHER_LOGLEVEL", "WARNING").upper()
    logger.setLevel(level)
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(filename)s > %(message)s")
    console.setFormatter(formatter)
    console.setLevel(level)
    # add the handlers to the logger
    logger.addHandler(console)
    logger.propagate = False
    return logger


def _init_logger(rank: int):
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        f"[{rank}] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def _init_logger(log_level=logging.INFO, log_format=None):
    """Initialize the logger.

    :param debug: Whether to enable debug mode
    :return: An instantiated logging instance
    """
    LOG.handlers = []

    if not log_format:
        # default log format
        log_format_string = constants.log_format_string
    else:
        log_format_string = log_format

    logging.captureWarnings(True)

    LOG.setLevel(log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(log_format_string))
    LOG.addHandler(handler)
    LOG.debug("logging initialized")

