from typing import Optional

def get_volcengine_headers(api_key: str, extra_headers: Optional[dict] = None) -> dict:
    """
    Get headers for Volcengine API calls.

    Args:
        api_key: The API key for authentication
        extra_headers: Optional additional headers

    Returns:
        Dictionary of headers
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    if extra_headers:
        headers.update(extra_headers)

    return headers

