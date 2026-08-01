
def phase_span(name: str) -> "Iterator[Span | None]":
    logger = _registered_v2_logger()
    if logger is None:
        yield None
        return
    with logger.start_phase_span(name) as span:
        yield span


def phase_span(name: str) -> "Iterator[Any]":
    """Run a request phase inside a live active span so its DB/service calls nest.

    Yields ``None`` (a plain no-op) when the OTel SDK is unavailable or V2 is not
    the active logger.
    """
    try:
        from litellm.integrations.otel.logger import phase_span as _phase_span
    except Exception:
        yield None
        return
    with _phase_span(name) as span:
        yield span

