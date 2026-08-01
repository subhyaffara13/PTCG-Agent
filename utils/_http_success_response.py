
def _http_success_response(response: httpx.Response) -> Dict[str, Any]:
    """Create a standardized success response from an httpx Response."""
    parsed_body: Any
    try:
        parsed_body = response.json()
    except (json.JSONDecodeError, ValueError):
        parsed_body = response.text

    return {
        "status_code": response.status_code,
        "body": parsed_body,
        "headers": dict(response.headers),
        "success": 200 <= response.status_code < 300,
        "error": None,
    }

