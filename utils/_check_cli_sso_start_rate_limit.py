
def _check_cli_sso_start_rate_limit(
    request: Request,
    cache: DualCache,
    use_x_forwarded_for: Optional[bool] = False,
) -> None:
    rate_limit_cache_key = _get_cli_sso_start_rate_limit_cache_key(
        request=request, use_x_forwarded_for=use_x_forwarded_for
    )
    current_attempts = cache.increment_cache(
        key=rate_limit_cache_key,
        value=1,
        ttl=_CLI_SSO_START_RATE_LIMIT_WINDOW_SECONDS,
    )
    if current_attempts > _CLI_SSO_START_RATE_LIMIT_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many CLI login attempts. Try again later.",
        )

