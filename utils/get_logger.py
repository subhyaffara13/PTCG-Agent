import logging
from typing import Any

def get_logger():
    return logging.getLogger(__name__)


def get_logger() -> logging.Logger | logging.LoggerAdapter[Any]:
    """Grab the global logger instance.

    If a global Application is instantiated, grab its logger.
    Otherwise, grab the root logger.
    """
    global _logger  # noqa: PLW0603

    if _logger is None:
        from .config import Application

        if Application.initialized():
            _logger = Application.instance().log
        else:
            _logger = logging.getLogger("traitlets")
            # Add a NullHandler to silence warnings about not being
            # initialized, per best practice for libraries.
            _logger.addHandler(logging.NullHandler())
    return _logger


def get_logger(name: str | None = None) -> TransformersLogger:
    """
    Return a logger with the specified name.

    This function is not supposed to be directly accessed unless you are writing a custom transformers module.
    """

    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    return logging.getLogger(name)


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Util function to set up a simple logger that writes
    into stderr. The loglevel is fetched from the LOGLEVEL
    env. variable or WARNING as default. The function will use the
    module name of the caller if no name is provided.

    Args:
        name: Name of the logger. If no name provided, the name will
              be derived from the call stack.
    """

    # Derive the name of the caller, if none provided
    # Use depth=2 since this function takes up one level in the call stack
    return _setup_logger(name or _derive_module_name(depth=2))


def getLogger(name: str) -> VerboseLogger:
    """logging.getLogger, but ensures our VerboseLogger class is returned"""
    return cast(VerboseLogger, logging.getLogger(name))


def get_logger(name, level=logging.DEBUG):
    logging.basicConfig(format="%(asctime)s %(name)s [%(levelname)s] - %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
        Returns a logger with the specified name. This function is not supposed
        to be directly accessed by library users.

        Args:
            name (`str`, *optional*):
                The name of the logger to get, usually the filename

        Example:

    ```python
    >>> from huggingface_hub import get_logger

    >>> logger = get_logger(__file__)
    >>> logger.set_verbosity_info()
    ```
    """

    if name is None:
        name = _get_library_name()

    return logging.getLogger(name)

