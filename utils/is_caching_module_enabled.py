
def IS_CACHING_MODULE_ENABLED() -> bool:
    """Check if the caching module is enabled.

    Returns False if:
    - The versioned config disables it
    - force_disable_caches is set in inductor config

    Returns:
        True if caching module is enabled, False otherwise.
    """
    if not _is_caching_module_enabled_base():
        return False
    if _is_force_disable_caches():
        return False
    return True

