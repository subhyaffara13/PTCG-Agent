import os
from typing import Dict

def _parse_generic_sso_headers() -> dict:
    """Parse comma-separated GENERIC_SSO_HEADERS env var into a dict."""
    raw = os.getenv("GENERIC_SSO_HEADERS", None)
    if raw is None:
        return {}
    result: Dict[str, str] = {}
    for header in raw.split(","):
        header = header.strip()
        if header:
            key, value = header.split("=")
            result[key] = value
    return result

