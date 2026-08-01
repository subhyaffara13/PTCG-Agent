
def get_unsupported_headers(provider: str) -> List[str]:
    """
    Get all beta headers that are unsupported by a provider (have null values in mapping).

    Args:
        provider: Provider name

    Returns:
        List of unsupported Anthropic beta header names
    """
    config = _load_beta_headers_config()
    provider = get_provider_name(provider)
    provider_mapping = config.get(provider, {})

    # Return headers with null values
    return [header for header, value in provider_mapping.items() if value is None]

