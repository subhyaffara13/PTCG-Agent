
def _cache_key(url: str, headers: dict[str, str], params: dict[str, str] | None, prefix: str | None = None) -> str:
    """Return a unique cache key for the given request parameters."""
    lower_headers = {k.lower(): v for k, v in headers.items()}  # casing is not guaranteed here
    auth_header = lower_headers.get("authorization", "")
    params_str = "&".join(f"{k}={v}" for k, v in sorted((params or {}).items(), key=lambda x: x[0]))
    return f"{prefix}|{url}|{auth_header}|{params_str}"

