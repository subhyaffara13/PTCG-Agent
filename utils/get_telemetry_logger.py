
def get_telemetry_logger(module: str) -> Callable[..., None]:
    """Return a module-labelled logger that forwards to the global exporter."""

    def logger(**kwargs: Any) -> None:
        _SEND(module=module, **kwargs)

    return logger

