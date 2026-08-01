
def set_telemetry_exporter(send_fn: TelemetrySendFn) -> None:
    """Inject a custom telemetry backend at runtime."""
    global _SEND
    _SEND = send_fn

