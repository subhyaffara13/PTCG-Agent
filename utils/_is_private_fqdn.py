import re

def _is_private_fqdn(host: str) -> bool:
    """
    Determine if an FQDN is likely to be internal/private.

    This uses heuristics based on RFC 952 and RFC 1123 standards:
    - .local domains (RFC 6762 - Multicast DNS)
    - .internal domains (common internal convention)
    - Single-label hostnames (no dots)
    - Common internal TLDs

    Args:
        host (str): The FQDN to check

    Returns:
        bool: True if the FQDN appears to be internal/private
    """
    host_lower = host.lower().rstrip(".")

    # Single-label hostnames (no dots) are typically internal
    if "." not in host_lower:
        return True

    # Common internal/private domain patterns
    internal_patterns = [
        r"\.local$",  # mDNS/Bonjour domains
        r"\.internal$",  # Common internal convention
        r"\.corp$",  # Corporate domains
        r"\.lan$",  # Local area network
        r"\.intranet$",  # Intranet domains
        r"\.private$",  # Private domains
    ]

    for pattern in internal_patterns:
        if re.search(pattern, host_lower):
            return True

    # If none of the internal patterns match, assume it's external
    return False

