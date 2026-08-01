
def _maybe_auto_initialize_arize_phoenix(_in_memory_loggers: list) -> None:
    """
    Auto-initialize ArizePhoenixLogger when Phoenix env vars are detected.

    Called during ``otel`` callback setup so that users get nested traces in
    both their OTEL collector *and* Arize Phoenix by only listing ``"otel"``
    in ``callbacks``.  If no Phoenix env vars are set, this is a no-op.
    """
    phoenix_env_vars = (
        "PHOENIX_API_KEY",
        "PHOENIX_COLLECTOR_HTTP_ENDPOINT",
        "PHOENIX_COLLECTOR_ENDPOINT",
    )
    if not any(os.environ.get(v) for v in phoenix_env_vars):
        return

    # Already registered — nothing to do
    if any(
        isinstance(cb, ArizePhoenixLogger) and cb.callback_name == "arize_phoenix"
        for cb in _in_memory_loggers
    ):
        return

    try:
        from litellm.integrations.opentelemetry import OpenTelemetryConfig

        arize_phoenix_config = ArizePhoenixLogger.get_arize_phoenix_config()
        otel_config = OpenTelemetryConfig(
            exporter=arize_phoenix_config.protocol,
            endpoint=arize_phoenix_config.endpoint,
            headers=arize_phoenix_config.otlp_auth_headers,
        )
        phoenix_logger = ArizePhoenixLogger(
            config=otel_config, callback_name="arize_phoenix"
        )
        _in_memory_loggers.append(phoenix_logger)

        # Register as a litellm callback so it receives success/failure events
        litellm.logging_callback_manager.add_litellm_callback(phoenix_logger)

        verbose_logger.info(
            "Auto-initialized Arize Phoenix logger alongside otel " "(endpoint=%s)",
            arize_phoenix_config.endpoint,
        )
    except Exception as e:
        verbose_logger.warning(
            "Failed to auto-initialize Arize Phoenix logger: %s", str(e)
        )

