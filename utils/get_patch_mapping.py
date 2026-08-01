
def get_patch_mapping() -> dict[str, type[nn.Module]]:
    """
    Get all registered patch mappings.

    Returns:
        `Dict[str, type[nn.Module]]`: Dictionary mapping class names or patterns to replacement classes.
    """
    with _monkey_patch_lock:
        return _monkey_patch_mapping_cache.copy()

