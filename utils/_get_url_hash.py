
def _get_url_hash(url: str) -> str:
    """Generate hash for URL to use as cache key."""
    return hashlib.sha256(url.encode()).hexdigest()

