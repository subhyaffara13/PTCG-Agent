
def _oauth_token_error(code: str, status: int = 400) -> JSONResponse:
    """RFC 6749 §5.2 token-endpoint error body: ``{"error": "<code>"}``.
    FastAPI's default ``HTTPException`` renders ``{"detail": ...}`` which
    spec-compliant OAuth clients parsing the ``error`` field won't recognize.
    """
    return JSONResponse(
        status_code=status, content={"error": code}, headers=TOKEN_NO_CACHE_HEADERS
    )

