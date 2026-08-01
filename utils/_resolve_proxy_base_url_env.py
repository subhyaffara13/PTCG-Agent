
def _resolve_proxy_base_url_env() -> Optional[str]:
    global _warned_invalid_proxy_base_url
    configured = os.environ.get("PROXY_BASE_URL", "").strip()
    if not configured:
        return None
    parsed = urlparse(configured)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        normalized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
        return normalized.rstrip("/")
    if _warned_invalid_proxy_base_url != configured:
        verbose_logger.warning(
            "PROXY_BASE_URL=%r is not a valid http(s) URL (missing scheme "
            "or host) and will be ignored for MCP OAuth origin resolution. "
            "Set it to a full URL like https://litellm.example.com.",
            configured,
        )
        _warned_invalid_proxy_base_url = configured
    return None

