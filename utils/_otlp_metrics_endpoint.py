
def _otlp_metrics_endpoint(endpoint: str | None) -> str | None:
    """Point an OTLP/HTTP base endpoint at the ``/v1/metrics`` signal path.

    The OTLP/HTTP exporter only appends ``/v1/metrics`` when it reads
    ``OTEL_EXPORTER_OTLP_ENDPOINT`` itself; an explicitly passed endpoint is used
    verbatim, so a base URL would POST to the root. Mirror ``_otlp_traces_endpoint``
    for the metrics signal (rewriting a sibling signal path when present).
    """
    if not endpoint:
        return endpoint
    endpoint = endpoint.rstrip("/")
    if endpoint.endswith("/v1/metrics"):
        return endpoint
    for other_signal in ("/v1/traces", "/v1/logs"):
        if endpoint.endswith(other_signal):
            return endpoint[: -len(other_signal)] + "/v1/metrics"
    return endpoint + "/v1/metrics"

