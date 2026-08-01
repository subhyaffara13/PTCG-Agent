
def _safe_get_response_text(response: httpx.Response) -> str:
    """Safely read response text, falling back to empty string on decoding errors."""
    try:
        return response.text
    except Exception:
        return ""

