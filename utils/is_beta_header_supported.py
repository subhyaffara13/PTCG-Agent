
def is_beta_header_supported(
    beta_header: str,
    provider: str,
) -> bool:
    """
    Check if a specific beta header is supported by a provider.

    Args:
        beta_header: The Anthropic beta header value
        provider: Provider name

    Returns:
        True if the header is in the mapping with a non-null value, False otherwise
    """
    config = _load_beta_headers_config()
    provider = get_provider_name(provider)
    provider_mapping = config.get(provider, {})

    # Header is supported if it's in the mapping and has a non-null value
    return beta_header in provider_mapping and provider_mapping[beta_header] is not None

