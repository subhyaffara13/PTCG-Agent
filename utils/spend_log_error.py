
def spend_log_error(
    message: str,
    *args: Any,
    exc: Optional[BaseException] = None,
) -> None:
    """Log a spend-tracking error, with the traceback gated on the env var.

    By default this behaves like ``verbose_proxy_logger.exception`` — the
    active exception (or ``exc`` if supplied) is attached so the formatter
    renders its traceback. When ``LITELLM_SUPPRESS_SPEND_LOG_TRACEBACKS`` is
    truthy and the logger is at INFO or above, the traceback is dropped and
    only ``message % args`` is emitted.

    Sentry / ``proxy_logging_obj.failure_handler`` is NOT invoked here — call
    sites still own the alerting path. This helper is purely about console /
    structured-log output volume.
    """
    if should_suppress_spend_log_tracebacks():
        verbose_proxy_logger.error(message, *args)
        return

    if exc is not None:
        verbose_proxy_logger.error(
            message, *args, exc_info=(type(exc), exc, exc.__traceback__)
        )
    else:
        verbose_proxy_logger.error(message, *args, exc_info=True)

