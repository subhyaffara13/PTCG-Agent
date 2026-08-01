
def _parse_bucket_id_from_url(url: str) -> str | None:
    """Extract bucket_id (namespace/name) from a bucket API URL."""
    match = _BUCKET_ID_FROM_URL_REGEX.search(url)
    return match.group(1) if match else None

