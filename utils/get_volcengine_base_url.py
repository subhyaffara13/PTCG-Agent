
def get_volcengine_base_url(api_base: Optional[str] = None) -> str:
    """
    Get the base URL for Volcengine API calls.

    Args:
        api_base: Optional custom API base URL

    Returns:
        The base URL to use for API calls
    """
    if api_base:
        return api_base
    return "https://ark.cn-beijing.volces.com"

