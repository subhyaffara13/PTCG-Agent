
def proxy_request_span_name(data: "ProxyRequestSpanData") -> str:
    """``"{method} {route}"`` (HTTP semconv)."""
    return f"{data.http_method} {data.route}".strip()

