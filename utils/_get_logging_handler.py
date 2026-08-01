
def _get_logging_handler(
    destination: str = _DEFAULT_DESTINATION,
) -> tuple[logging.Handler, str]:
    log_handler = _log_handlers[destination]
    log_handler_name = f"{type(log_handler).__name__}-{destination}"
    return (log_handler, log_handler_name)


def _get_logging_handler(
    destination: str = "default",
) -> tuple[logging.Handler, str]:
    log_handler = _log_handlers[destination]
    log_handler_name = type(log_handler).__name__
    return (log_handler, log_handler_name)

