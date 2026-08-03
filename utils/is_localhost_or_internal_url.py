from typing import Optional

def is_localhost_or_internal_url(url: Optional[str]) -> bool:
    """
    Check if a URL is a localhost or internal URL.

    This detects common development URLs that are accidentally left in
    agent cards when deploying to production.

    Args:
        url: The URL to check

    Returns:
        True if the URL is localhost/internal
    """
    if not url:
        return False

    url_lower = url.lower()

    return any(pattern in url_lower for pattern in LOCALHOST_URL_PATTERNS)

