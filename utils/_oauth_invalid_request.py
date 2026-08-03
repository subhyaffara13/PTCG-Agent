from typing import Any, Dict, Optional

def _oauth_invalid_request(
    error_description: str,
    *,
    hint: Optional[str] = None,
    **extra: Any,
) -> NoReturn:
    """Raise ``invalid_request`` (RFC 6749) with a debuggable description.

    FastAPI serializes ``detail`` as JSON. Callers still see ``error``:
    ``invalid_request``; ``error_description`` and ``hint`` explain what
    failed and how to fix it (e.g. reverse-proxy / PROXY_BASE_URL issues).
    """
    detail: Dict[str, Any] = {
        "error": "invalid_request",
        "error_description": error_description,
    }
    if hint:
        detail["hint"] = hint
    detail.update(extra)
    raise HTTPException(status_code=400, detail=detail)

