
def _disable_debugging():
    """Disable the package, router, and proxy verbose loggers."""
    verbose_logger.disabled = True
    verbose_router_logger.disabled = True
    verbose_proxy_logger.disabled = True

