
def _authorize_drain_request(request: Request) -> None:
    """
    Reject /health/drain calls that don't carry the configured X-Drain-Token.

    When no token is configured the endpoint is treated as already opted-in
    (the ``enable_drain_endpoint`` flag is the only gate). Comparison uses
    ``secrets.compare_digest`` to avoid timing leaks.
    """
    expected = _drain_endpoint_token()
    if expected is None:
        return
    supplied = request.headers.get("x-drain-token") or ""
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Drain-Token",
        )

