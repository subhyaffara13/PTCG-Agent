
def add_provider_specific_headers_to_request(
    data: dict,
    headers: dict,
):
    from litellm.llms.anthropic.common_utils import is_anthropic_oauth_key

    anthropic_headers = {}
    # boolean to indicate if a header was added
    added_header = False
    for header in ANTHROPIC_API_HEADERS:
        if header in headers:
            header_value = headers[header]
            anthropic_headers[header] = header_value
            added_header = True

    # Check for Authorization header with Anthropic OAuth token (sk-ant-oat*)
    # This needs to be handled via provider-specific headers to ensure it only
    # goes to Anthropic-compatible providers, not all providers in the router
    for header, value in headers.items():
        if header.lower() == "authorization" and is_anthropic_oauth_key(value):
            anthropic_headers[header] = value
            added_header = True
            break
    if added_header is True:
        # Anthropic headers work across multiple providers
        # Store as comma-separated list so retrieval can match any of them
        data["provider_specific_header"] = ProviderSpecificHeader(
            custom_llm_provider=f"{LlmProviders.ANTHROPIC.value},{LlmProviders.BEDROCK.value},{LlmProviders.VERTEX_AI.value}",
            extra_headers=anthropic_headers,
        )

    return

