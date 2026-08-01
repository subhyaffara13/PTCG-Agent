
def reload_beta_headers_config() -> Dict:
    """
    Force reload the beta headers configuration from source (remote or local).
    Clears the cache and fetches fresh configuration.

    Returns:
        Dict containing the newly loaded beta headers configuration
    """
    global _BETA_HEADERS_CONFIG
    _BETA_HEADERS_CONFIG = None
    verbose_logger.info("Reloading beta headers config (cache cleared)")
    return _load_beta_headers_config()

