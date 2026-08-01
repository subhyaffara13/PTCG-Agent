
def _get_cli_sso_flow_cache_key(login_id: str) -> str:
    return f"{_CLI_SSO_FLOW_CACHE_KEY_PREFIX}:{login_id}"

