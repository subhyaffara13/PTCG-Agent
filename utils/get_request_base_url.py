
def get_request_base_url(request: Request) -> str:
    """
    Get the base URL for the request, considering X-Forwarded-* headers.

    Resolution order: ``PROXY_BASE_URL`` env var, then X-Forwarded-* when
    the caller is a trusted proxy (``use_x_forwarded_for`` enabled AND
    caller in ``mcp_trusted_proxy_ranges``), otherwise the request's
    literal ``base_url``. Untrusted callers cannot poison OAuth-discovery
    / redirect_uri values by injecting headers.
    """
    configured = _resolve_proxy_base_url_env()
    if configured:
        return configured

    base_url = str(request.base_url).rstrip("/")
    parsed = urlparse(base_url)

    if not IPAddressUtils.is_request_from_trusted_proxy(request):
        return base_url

    x_forwarded_proto = request.headers.get("X-Forwarded-Proto")
    x_forwarded_host = request.headers.get("X-Forwarded-Host")
    x_forwarded_port = request.headers.get("X-Forwarded-Port")

    scheme = x_forwarded_proto if x_forwarded_proto else parsed.scheme

    if x_forwarded_host:
        # X-Forwarded-Host may already include port (e.g., "example.com:8080")
        if ":" in x_forwarded_host and not x_forwarded_host.startswith("["):
            netloc = x_forwarded_host
        elif x_forwarded_port:
            netloc = f"{x_forwarded_host}:{x_forwarded_port}"
        else:
            netloc = x_forwarded_host
    else:
        netloc = parsed.netloc
        if x_forwarded_port and ":" not in netloc:
            netloc = f"{netloc}:{x_forwarded_port}"

    return urlunparse((scheme, netloc, parsed.path, "", "", ""))

