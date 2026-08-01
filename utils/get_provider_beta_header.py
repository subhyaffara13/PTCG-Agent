
def get_provider_beta_header(
    anthropic_beta_header: str,
    provider: str,
) -> Optional[str]:
    """
    Get the provider-specific beta header name for a given Anthropic beta header.

    This function handles header transformations/mappings (e.g., advanced-tool-use -> tool-search-tool).

    Args:
        anthropic_beta_header: The Anthropic beta header value
        provider: Provider name

    Returns:
        The provider-specific header name if supported, or None if unsupported/unknown
    """
    config = _load_beta_headers_config()
    provider = get_provider_name(provider)

    # Get the header mapping for this provider
    provider_mapping = config.get(provider, {})

    # Check if header is in the mapping
    if anthropic_beta_header not in provider_mapping:
        return None

    # Return the mapped value (could be None if unsupported)
    return provider_mapping[anthropic_beta_header]

