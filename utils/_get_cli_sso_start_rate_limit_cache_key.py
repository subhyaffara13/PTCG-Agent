from typing import Optional

def _get_cli_sso_start_rate_limit_cache_key(
    request: Request, use_x_forwarded_for: Optional[bool] = False
) -> str:
    client_ip = (
        _get_request_ip_address(
            request=request, use_x_forwarded_for=use_x_forwarded_for
        )
        or "unknown"
    )
    client_ip_hash = _hash_cli_sso_secret(client_ip)
    return f"{_CLI_SSO_START_RATE_LIMIT_CACHE_KEY_PREFIX}:{client_ip_hash}"

