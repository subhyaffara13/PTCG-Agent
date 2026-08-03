from typing import Any, Dict

def _http_error_response(error: str) -> Dict[str, Any]:
    """Create a standardized error response for HTTP requests."""
    return {
        "status_code": 0,
        "body": None,
        "headers": {},
        "success": False,
        "error": error,
    }

