
def _matches_trusted_origin_entry(netloc: str, entry: str) -> bool:
    """``entry`` is either ``host[:port]`` (exact match after port
    normalization) or ``*.suffix`` (subdomain wildcard; matches any
    strictly-deeper subdomain of ``suffix`` but not ``suffix`` itself).
    ``netloc`` is the already-port-normalized, lowercased netloc of
    the redirect_uri being validated.
    """
    if entry.startswith("*."):
        suffix = entry[2:]
        if not suffix or suffix.startswith("."):
            return False
        # Strip port from netloc for wildcard host comparison;
        # wildcards don't express port constraints.
        host = netloc.split(":", 1)[0] if ":" in netloc else netloc
        return host != suffix and host.endswith("." + suffix)
    return netloc == entry

