from typing import Optional

def optionally_handle_anthropic_oauth(
    headers: dict, api_key: Optional[str]
) -> tuple[dict, Optional[str]]:
    """
    Handle Anthropic OAuth token detection and header setup.

    If an OAuth token is detected in the Authorization header, extracts it
    and sets the required OAuth headers.

    Args:
        headers: Request headers dict
        api_key: Current API key (may be None)

    Returns:
        Tuple of (updated headers, api_key)
    """
    # Check Authorization header (passthrough / forwarded requests)
    auth_header = headers.get("authorization", "")
    if auth_header and auth_header.startswith(f"Bearer {ANTHROPIC_OAUTH_TOKEN_PREFIX}"):
        api_key = auth_header.replace("Bearer ", "")
        headers.pop("x-api-key", None)
        headers["anthropic-beta"] = _merge_beta_headers(
            headers.get("anthropic-beta"), ANTHROPIC_OAUTH_BETA_HEADER
        )
        headers["anthropic-dangerous-direct-browser-access"] = "true"
        return headers, api_key
    # Check api_key directly (standard chat/completion flow)
    if api_key and api_key.startswith(ANTHROPIC_OAUTH_TOKEN_PREFIX):
        headers.pop("x-api-key", None)
        headers["authorization"] = f"Bearer {api_key}"
        headers["anthropic-beta"] = _merge_beta_headers(
            headers.get("anthropic-beta"), ANTHROPIC_OAUTH_BETA_HEADER
        )
        headers["anthropic-dangerous-direct-browser-access"] = "true"
    return headers, api_key

