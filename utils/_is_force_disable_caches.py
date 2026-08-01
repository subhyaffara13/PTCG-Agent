
def _is_force_disable_caches() -> bool:
    """Check if caching is force disabled via inductor config.

    This defers importing torch._inductor.config to avoid circular imports.

    Returns:
        True if force_disable_caches is set in inductor config, False otherwise.
    """
    from torch._inductor import config as inductor_config

    return inductor_config.force_disable_caches

