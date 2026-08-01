
def _safe_emit(label: str, fn, *args, **kwargs) -> None:
    """Run an additive attribute emitter, swallowing any error so it cannot
    blank attributes set elsewhere on the span. Failures are logged at debug.
    """
    try:
        fn(*args, **kwargs)
    except Exception as e:
        verbose_logger.debug("[Arize] %s skipped: %s", label, e)

