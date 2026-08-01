
def clear_patch_mapping() -> None:
    """
    Clear all registered patch mappings.

    This removes all registered mappings from the global registry.

    Example:
        ```python
        from transformers.monkey_patching import register_patch_mapping, clear_patch_mapping

        # Register some patches
        register_patch_mapping(
            mapping={"Qwen2MoeExperts": CustomExperts}
        )

        # Clear all patches
        clear_patch_mapping()
        ```
    """
    global _monkey_patch_mapping_cache
    with _monkey_patch_lock:
        _monkey_patch_mapping_cache.clear()

