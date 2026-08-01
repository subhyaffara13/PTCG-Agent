
def _extract_proxy_litellm_metadata(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return ``kwargs["litellm_metadata"]`` when it's a dict; ``None`` otherwise.

    The proxy attaches its auth/spend-attribution fields (``user_api_key``,
    ``user_api_key_team_id``, ``litellm_call_id``, the full ``UserAPIKeyAuth``
    object under ``user_api_key_auth``, ...) to ``data["litellm_metadata"]``
    for ``/v1/messages`` (see
    ``LiteLLMProxyRequestSetup.add_user_api_key_auth_to_request_metadata`` and
    ``LITELLM_METADATA_ROUTES``). The Anthropic-shape ``metadata`` arg only
    carries ``user_id`` and must not be conflated. Returns ``None`` for SDK
    callers that bypass the proxy entirely.
    """
    litellm_metadata = kwargs.get("litellm_metadata")
    if not isinstance(litellm_metadata, dict):
        return None
    return litellm_metadata

