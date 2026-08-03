from typing import Optional

def get_url_domain(url: str) -> Optional[str]:
    """
    Extract the domain from a URL.

    Args:
        url: The URL to parse

    Returns:
        The domain, or None if invalid
    """
    try:
        result = urlparse(url)
        return result.netloc if result.netloc else None
    except Exception:
        return None

