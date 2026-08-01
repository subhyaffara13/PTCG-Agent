
def is_valid_url(url: str) -> bool:
    """
    Check if a URL is syntactically valid.

    Args:
        url: The URL to validate

    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

