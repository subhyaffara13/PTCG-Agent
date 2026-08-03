import logging
import os

def _setup_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOGLEVEL", get_log_level()))
    return logger


def _setup_logger(verbose):
    if verbose:
        logging.basicConfig(
            format="[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(format="%(funcName)20s: %(message)s", level=logging.INFO)


def _setup_logger(verbose):
    if verbose:
        logging.basicConfig(
            format="[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s", level=logging.DEBUG, force=True
        )
    else:
        logging.basicConfig(format="%(funcName)20s: %(message)s", level=logging.INFO, force=True)

