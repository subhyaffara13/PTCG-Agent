
def get_stored_api_key(expected_base_url: Optional[str] = None) -> Optional[str]:
    """Get the stored API key from token file.

    If expected_base_url is provided, the key is only returned when it was
    originally issued for that URL. This prevents credential leakage when the
    CLI is pointed at a different (possibly malicious) server.
    """
    from litellm.litellm_core_utils.cli_token_utils import get_litellm_gateway_api_key

    return get_litellm_gateway_api_key(expected_base_url=expected_base_url)

