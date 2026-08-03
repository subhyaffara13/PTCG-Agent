from typing import Tuple

def validate_url(url: str) -> Tuple[str, str]:
    """
    Validate a user-supplied URL and rewrite it to connect to a validated IP.

    Resolves the hostname, checks all resolved IPs against blocked networks,
    then returns a rewritten URL that points to the validated IP along with
    the original hostname (for use in the Host header).

    This eliminates DNS rebinding because the caller connects to the IP we
    validated, not the hostname that could rebind. Callers should also disable
    follow_redirects to prevent redirect-based SSRF bypasses.

    Args:
        url: The user-supplied URL to validate.

    Returns:
        Tuple of (rewritten_url, host_header).
        The rewritten URL has the hostname replaced with the validated IP.
        The host_header value should be sent as the Host header.

    Raises:
        SSRFError: If the URL scheme is invalid or the hostname resolves
            to a private/internal IP address.
    """
    parsed = urlparse(url)

    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise SSRFError(f"URL scheme '{parsed.scheme}' is not allowed")

    hostname = parsed.hostname
    if not hostname:
        raise SSRFError("URL has no hostname")

    port = parsed.port
    default_port = _default_port_for_scheme(parsed.scheme)
    effective_port = port if port is not None else default_port
    host_header = _format_host_header(hostname, effective_port, default_port)

    is_allowlisted = _is_host_allowlisted(hostname, effective_port)

    # Resolve hostname and validate ALL addresses
    try:
        addrinfo = socket.getaddrinfo(
            hostname, effective_port, proto=socket.IPPROTO_TCP
        )
    except socket.gaierror as e:
        raise SSRFError(f"DNS resolution failed for '{hostname}': {e}")

    if not addrinfo:
        raise SSRFError(f"No addresses found for '{hostname}'")

    if not is_allowlisted:
        for family, type_, proto, canonname, sockaddr in addrinfo:
            resolved_ip = _sockaddr_host(sockaddr)
            if _is_blocked_ip(resolved_ip):
                raise SSRFError(
                    f"URL targets a blocked address ({resolved_ip}). "
                    "If this is a legitimate internal service, add the host "
                    "to `user_url_allowed_hosts` in general_settings."
                )

    # For HTTPS with SSL verification enabled, TLS certificate validation
    # binds the connection to the hostname — DNS rebinding can't redirect
    # to a different server because the cert wouldn't match.
    # When SSL verification is disabled, this defense doesn't apply, so
    # we rewrite to the validated IP like HTTP.
    ssl_verify = getattr(litellm, "ssl_verify", True)
    if parsed.scheme == "https" and ssl_verify is not False:
        return url, host_header

    # For HTTP, rewrite URL to connect to the validated IP directly
    # to prevent DNS rebinding (no TLS to bind the connection).
    validated_ip = _sockaddr_host(addrinfo[0][4])
    is_ipv6 = addrinfo[0][0] == socket.AF_INET6
    ip_host = f"[{validated_ip}]" if is_ipv6 else validated_ip

    if port is not None:
        new_netloc = f"{ip_host}:{port}"
    else:
        new_netloc = ip_host

    rewritten = urlunparse(
        (parsed.scheme, new_netloc, parsed.path, parsed.params, parsed.query, "")
    )

    return rewritten, host_header

