
def _set_cli_sso_flow(login_id: str, cache: DualCache, flow: dict) -> None:
    cache.set_cache(
        key=_get_cli_sso_flow_cache_key(login_id),
        value=flow,
        ttl=CLI_SSO_SESSION_TTL_SECONDS,
    )

