
def _get_otel_v2_class() -> Optional[type]:
    """Return the ``OpenTelemetryV2`` class, or ``None`` if the OTel SDK is absent.

    Imported lazily: ``litellm.integrations.otel.logger`` imports the OpenTelemetry
    SDK at module scope, so importing it eagerly would break installs without the
    SDK. The V2 logger only exists when ``LITELLM_OTEL_V2`` is enabled (which
    requires the SDK), so a failed import simply means "no V2 logger in play".
    """
    try:
        from litellm.integrations.otel.logger import OpenTelemetryV2

        return OpenTelemetryV2
    except Exception:
        return None

