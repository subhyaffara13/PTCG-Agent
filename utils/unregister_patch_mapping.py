
def unregister_patch_mapping(keys: list[str]) -> None:
    """
    Unregister patch mappings to disable automatic patching.

    This removes specified mappings from the global registry, preventing them from being applied
    during model loading. You must provide the exact same name or pattern that was used during registration.

    Args:
        keys (`List[str]`):
            List of mapping keys (class names or regex patterns) to remove from the patch mapping
            (e.g., `["Qwen2MoeExperts"]` or `[".*Attention"]`).

    Example:
        ```python
        from transformers import AutoModelForCausalLM
        from transformers.monkey_patching import register_patch_mapping, unregister_patch_mapping

        # Register a patch
        register_patch_mapping(
            mapping={"Qwen2MoeExperts": CustomExperts}
        )

        # Unregister the patch
        unregister_patch_mapping(["Qwen2MoeExperts"])

        # The patch will no longer be applied during loading
        model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-MoE-A2.7B")
        ```
    """
    global _monkey_patch_mapping_cache
    with _monkey_patch_lock:
        for key in keys:
            if key not in _monkey_patch_mapping_cache:
                raise ValueError(
                    f"Class or pattern '{key}' not found in monkey patch mapping cache. "
                    f"Cannot unregister a class that is not registered."
                )
            del _monkey_patch_mapping_cache[key]

