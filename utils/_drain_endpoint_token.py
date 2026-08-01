
def _drain_endpoint_token() -> Optional[str]:
    """
    Shared secret required on the X-Drain-Token header to call /health/drain.

    Falls back to the ``DRAIN_ENDPOINT_TOKEN`` env var when unset in
    general_settings so the kubelet preStop hook can supply it via
    ``valueFrom.secretKeyRef`` without a config reload.
    """
    from litellm.proxy.proxy_server import general_settings

    token = general_settings.get("drain_endpoint_token")
    if isinstance(token, str) and token:
        return token
    env_token = os.getenv("DRAIN_ENDPOINT_TOKEN")
    if env_token:
        return env_token
    return None

