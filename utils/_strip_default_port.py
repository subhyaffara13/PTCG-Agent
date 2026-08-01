
def _strip_default_port(scheme: str, netloc: str) -> str:
    """Return ``netloc`` lowercased with the scheme's default port
    stripped. ``Llm.Example.com:443`` with scheme ``https`` becomes
    ``llm.example.com``. Used so a literal netloc comparison between
    the proxy's origin and the client redirect_uri survives a load-
    balancer that sets ``X-Forwarded-Port: 443``.
    """
    if not netloc:
        return netloc
    lowered = netloc.lower()
    if lowered.startswith("["):
        # IPv6 literal: port (if any) appears after the "]".
        close = lowered.rfind("]")
        if close != -1 and lowered[close + 1 :].startswith(":"):
            try:
                port = int(lowered[close + 2 :])
            except ValueError:
                return lowered
            if _DEFAULT_PORTS.get(scheme) == port:
                return lowered[: close + 1]
        return lowered
    if ":" in lowered:
        host, _, port_str = lowered.rpartition(":")
        try:
            port = int(port_str)
        except ValueError:
            return lowered
        if _DEFAULT_PORTS.get(scheme) == port:
            return host
    return lowered

