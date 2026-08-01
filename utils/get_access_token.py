
def get_access_token(
    credentials: Optional[str] = None,
    scope: Optional[str] = None,
    auth_url: Optional[str] = None,
) -> str:
    """
    Get valid access token, using cache if available.

    Args:
        credentials: Base64-encoded credentials (client_id:client_secret)
        scope: API scope (GIGACHAT_API_PERS, GIGACHAT_API_CORP, etc.)
        auth_url: OAuth endpoint URL

    Returns:
        Access token string

    Raises:
        GigaChatAuthError: If authentication fails
    """
    credentials = credentials or _get_credentials()
    if not credentials:
        raise GigaChatAuthError(
            status_code=401,
            message="GigaChat credentials not provided. Set GIGACHAT_CREDENTIALS or GIGACHAT_API_KEY environment variable.",
        )

    scope = scope or _get_scope()
    auth_url = auth_url or _get_auth_url()

    # Check cache
    cache_key = f"gigachat_token:{credentials[:16]}"
    cached = _token_cache.get_cache(cache_key)
    if cached:
        token, expires_at = cached
        # Check if token is still valid (with buffer)
        if time.time() * 1000 < expires_at - TOKEN_EXPIRY_BUFFER_MS:
            verbose_logger.debug("Using cached GigaChat access token")
            return token

    # Request new token
    token, expires_at = _request_token_sync(credentials, scope, auth_url)

    # Cache token
    ttl_seconds = max(
        0, (expires_at - TOKEN_EXPIRY_BUFFER_MS - time.time() * 1000) / 1000
    )
    if ttl_seconds > 0:
        _token_cache.set_cache(cache_key, (token, expires_at), ttl=ttl_seconds)

    return token

