
def get_litellm_gateway_api_key(
    expected_base_url: Optional[str] = None,
) -> Optional[str]:
    """
    Get the stored CLI API key for use with LiteLLM SDK.

    This function reads the token file created by `lite login`
    and returns the API key for use in Python scripts.

    Args:
        expected_base_url: When provided, the key is only returned if it was
            originally issued for this URL. Pass the target server URL to
            prevent credential leakage when the client is pointed at a
            different (possibly malicious) server.

    Returns:
        str: The API key if found (and origin matches), None otherwise

    Example:
        >>> import litellm
        >>> api_key = litellm.get_litellm_gateway_api_key()
        >>> if api_key:
        >>>     response = litellm.completion(
        >>>         model="gpt-3.5-turbo",
        >>>         messages=[{"role": "user", "content": "Hello"}],
        >>>         api_key=api_key,
        >>>         base_url="https://your-proxy.com/v1"
        >>>     )
    """
    token_data = load_cli_token()
    if not token_data or "key" not in token_data:
        return None
    if expected_base_url is not None:
        stored_url = token_data.get("base_url")
        if stored_url != expected_base_url.rstrip("/"):
            return None
    return token_data["key"]

