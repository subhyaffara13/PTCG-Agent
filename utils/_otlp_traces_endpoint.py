
def _otlp_traces_endpoint(endpoint: str | None) -> str | None:
    """Point an OTLP/HTTP base endpoint at the ``/v1/traces`` signal path.

    ``OTEL_EXPORTER_OTLP_ENDPOINT`` is a base URL (e.g. ``http://host:4318``).
    The OTLP/HTTP exporter only appends the ``/v1/traces`` path when it reads
    that env var itself; when an endpoint is passed explicitly it is used
    verbatim, so a base URL would POST to the root and the collector returns
    404. Append the signal path here (leaving an already-correct path intact).
    """
    if not endpoint:
        return endpoint
    endpoint = endpoint.rstrip("/")
    # Splunk Observability uses ``/v2/trace/otlp``; never rewrite it.
    if endpoint.endswith("/v1/traces") or "/v2/trace/otlp" in endpoint:
        return endpoint
    for other_signal in ("/v1/logs", "/v1/metrics"):
        if endpoint.endswith(other_signal):
            return endpoint[: -len(other_signal)] + "/v1/traces"
    return endpoint + "/v1/traces"

