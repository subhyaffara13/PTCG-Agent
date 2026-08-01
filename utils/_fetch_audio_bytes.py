
def _fetch_audio_bytes(url: str, timeout: float | None = 10.0) -> bytes:
    """Fetch audio bytes from a URL with automatic retry and exponential backoff."""
    response = httpx.get(url, follow_redirects=True, timeout=timeout)
    response.raise_for_status()
    return response.content

