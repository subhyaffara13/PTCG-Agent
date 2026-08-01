
def _load_beta_headers_config() -> Dict:
    """
    Load the beta headers configuration.
    Uses caching to avoid repeated fetches/file reads.

    This function is called by all public API functions and manages the global cache.

    Returns:
        Dict containing the beta headers configuration
    """
    global _BETA_HEADERS_CONFIG

    if _BETA_HEADERS_CONFIG is not None:
        return _BETA_HEADERS_CONFIG

    # Get the URL from environment or use default
    from litellm import anthropic_beta_headers_url

    _BETA_HEADERS_CONFIG = get_beta_headers_config(url=anthropic_beta_headers_url)
    verbose_logger.debug("Loaded and cached beta headers config")

    return _BETA_HEADERS_CONFIG

