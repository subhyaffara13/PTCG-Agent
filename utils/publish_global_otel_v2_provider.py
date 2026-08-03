from typing import Callable

def publish_global_otel_v2_provider(
    in_memory_loggers: Sequence[object],
    set_global_provider: Callable[[TracerProvider], None],
    registered: "OpenTelemetryV2 | None" = None,
) -> "OpenTelemetryV2":
    """Select the single v2 logger and publish its provider as the OTel global.

    The proxy calls this once at startup, after callbacks are initialized, so the
    preset logger already exists; it passes ``registered`` (the canonical owner the
    factory designated as ``proxy_server.open_telemetry_logger``) so the global
    provider reuses the same logger the rest of the v2 code emits through (see
    :func:`select_global_otel_v2_logger`). Both ``registered`` and
    ``set_global_provider`` (the proxy passes
    ``opentelemetry.trace.set_tracer_provider``) are injected so the publish step is
    unit-testable without reading or mutating real global OTel state. Returns the
    logger whose provider was published.
    """
    logger = select_global_otel_v2_logger(in_memory_loggers, registered=registered)
    set_global_provider(logger._tracer_provider)
    return logger

