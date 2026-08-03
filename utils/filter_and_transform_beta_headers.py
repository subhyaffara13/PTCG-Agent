from typing import List, Set

def filter_and_transform_beta_headers(
    beta_headers: List[str],
    provider: str,
) -> List[str]:
    """
    Filter and transform beta headers based on provider's mapping configuration.

    This function:
    1. Only allows headers that are present in the provider's mapping keys
    2. Filters out headers with null values (unsupported)
    3. Maps headers to provider-specific names (e.g., advanced-tool-use -> tool-search-tool)

    Args:
        beta_headers: List of Anthropic beta header values
        provider: Provider name (e.g., "anthropic", "bedrock", "vertex_ai")

    Returns:
        List of filtered and transformed beta headers for the provider
    """
    if not beta_headers:
        return []

    config = _load_beta_headers_config()
    provider = get_provider_name(provider)

    # Get the header mapping for this provider
    provider_mapping = config.get(provider, {})

    filtered_headers: Set[str] = set()

    for header in beta_headers:
        header = header.strip()

        # Check if header is in the mapping
        if header not in provider_mapping:
            verbose_logger.debug(
                f"Dropping unknown beta header '{header}' for provider '{provider}' (not in mapping)"
            )
            continue

        # Get the mapped header value
        mapped_header = provider_mapping[header]

        # Skip if header is unsupported (null value)
        if mapped_header is None:
            verbose_logger.debug(
                f"Dropping unsupported beta header '{header}' for provider '{provider}'"
            )
            continue

        # Add the mapped header
        filtered_headers.add(mapped_header)

    return sorted(list(filtered_headers))

