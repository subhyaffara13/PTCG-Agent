
def _get_cli_sso_flow_or_raise(login_id: Optional[str], cache: DualCache) -> dict:
    if not _is_valid_cli_sso_login_id(login_id):
        raise HTTPException(status_code=400, detail="Invalid CLI login session")

    cache_key = _get_cli_sso_flow_cache_key(cast(str, login_id))
    flow = cache.get_cache(key=cache_key)
    if not isinstance(flow, dict) or "poll_secret_hash" not in flow:
        raise HTTPException(status_code=400, detail="Invalid CLI login session")
    return flow

