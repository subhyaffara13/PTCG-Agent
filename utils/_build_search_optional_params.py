
def _build_search_optional_params(
    max_results: Optional[int] = None,
    search_domain_filter: Optional[List[str]] = None,
    max_tokens_per_page: Optional[int] = None,
    country: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Helper function to build optional_params dict from Perplexity Search API parameters.

    Args:
        max_results: Maximum number of results (1-20)
        search_domain_filter: List of domains to filter (max 20)
        max_tokens_per_page: Max tokens per page
        country: Country code filter

    Returns:
        Dict with non-None optional parameters
    """
    optional_params: Dict[str, Any] = {}

    if max_results is not None:
        optional_params["max_results"] = max_results
    if search_domain_filter is not None:
        optional_params["search_domain_filter"] = search_domain_filter
    if max_tokens_per_page is not None:
        optional_params["max_tokens_per_page"] = max_tokens_per_page
    if country is not None:
        optional_params["country"] = country

    return optional_params

