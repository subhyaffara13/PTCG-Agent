
def _format_host_header(hostname: str, port: int, default_port: int) -> str:
    """Build an RFC 7230 Host header value, bracketing IPv6 literals."""
    bracketed = f"[{hostname}]" if ":" in hostname else hostname
    if port == default_port:
        return bracketed
    return f"{bracketed}:{port}"

