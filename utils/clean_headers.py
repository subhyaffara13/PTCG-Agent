
def clean_headers(
    headers: Headers,
    litellm_key_header_name: Optional[str] = None,
    forward_llm_provider_auth_headers: bool = False,
    authenticated_with_header: Optional[str] = None,
) -> dict:
    """
    Removes litellm api key from headers

    Args:
        headers: Request headers
        litellm_key_header_name: Custom header name for LiteLLM API key
        forward_llm_provider_auth_headers: Whether to forward provider auth headers
        authenticated_with_header: Which header was used for LiteLLM authentication
            (e.g., "x-litellm-api-key", "authorization", "x-api-key")

    Returns:
        Cleaned headers dict
    """
    from litellm.llms.anthropic.common_utils import is_anthropic_oauth_key

    clean_headers = {}
    litellm_key_lower = (
        litellm_key_header_name.lower() if litellm_key_header_name is not None else None
    )
    for header, value in headers.items():
        header_lower = header.lower()

        if header_lower == "authorization" and is_anthropic_oauth_key(value):
            if (
                authenticated_with_header is None
                or authenticated_with_header.lower() != "authorization"
            ):
                clean_headers[header] = value
            continue
        # Special handling for x-api-key: forward it based on authenticated_with_header
        elif header_lower == "x-api-key":
            if forward_llm_provider_auth_headers and (
                authenticated_with_header is None
                or authenticated_with_header.lower() != "x-api-key"
            ):
                clean_headers[header] = value
        elif (
            forward_llm_provider_auth_headers and header_lower in _SPECIAL_HEADERS_CACHE
        ):
            if litellm_key_lower and header_lower == litellm_key_lower:
                continue
            if header_lower == "authorization":
                continue
            # Never forward x-litellm-api-key (it's for proxy auth only)
            if header_lower == "x-litellm-api-key":
                continue
            clean_headers[header] = value
        # Check if header should be excluded: either in special headers cache or matches custom litellm key
        elif header_lower not in _SPECIAL_HEADERS_CACHE and (
            litellm_key_lower is None or header_lower != litellm_key_lower
        ):
            clean_headers[header] = value
    return clean_headers

