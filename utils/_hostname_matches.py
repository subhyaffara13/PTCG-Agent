
def _hostname_matches(hostname: str, suffixes: tuple) -> bool:
    """True if hostname equals one of `suffixes` or is a subdomain of it.

    Uses suffix matching (not a bare substring test) so look-alikes such as
    `cognitiveservices.azure.com.attacker.example` are not accepted.
    """
    return any(
        hostname == suffix or hostname.endswith("." + suffix) for suffix in suffixes
    )

