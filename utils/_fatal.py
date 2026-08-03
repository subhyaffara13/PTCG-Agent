import sys

def _fatal(msg: str) -> NoReturn:  # pragma: no cover
    """
    Log a fatal error to the standard error stream and exit.
    """
    # NOTE: We buffer the logger when the progress spinner is active,
    # ensuring that the fatal message is formatted on its own line.
    logger.error(msg)
    sys.exit(1)

