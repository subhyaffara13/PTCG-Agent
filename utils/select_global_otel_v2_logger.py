
def select_global_otel_v2_logger(
    in_memory_loggers: Sequence[object],
    registered: "OpenTelemetryV2 | None" = None,
) -> "OpenTelemetryV2":
    """The single ``OpenTelemetryV2`` whose provider should become the OTel global.

    The callback factory designates one logger as canonical the moment it builds
    the first one (``_init_otel_logger_on_litellm_proxy`` sets
    ``proxy_server.open_telemetry_logger``), and every other v2 entry point —
    guardrail, identity seeding, phase spans — already routes through that same
    ``registered`` owner. Reuse it here too so the global provider has one source
    of truth instead of a second, independently-derived guess; this is the logger
    a preset (arize, langfuse, …) folds the ``OTEL_*`` base exporter and its own
    exporter into, so the FastAPI server span and the gen-ai spans share one
    provider and one trace.

    Fall back to ``in_memory_loggers`` for the SDK path, where no proxy global is
    set (selecting from there, not ``service_callback``, which a preset logger does
    not always reach), and build a generic logger from ``OTEL_*`` only when none was
    configured at all. Each fallback still avoids the second generic logger that
    orphaned the gen-ai spans onto a different backend than the server span.
    """
    if registered is not None:
        return registered
    existing = next(
        (cb for cb in in_memory_loggers if isinstance(cb, OpenTelemetryV2)), None
    )
    return existing if existing is not None else OpenTelemetryV2()

