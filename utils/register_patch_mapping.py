
def register_patch_mapping(mapping: dict[str, type[nn.Module]], overwrite: bool = False) -> None:
    """
    Register patch mappings to enable automatic patching during model creation using `from_pretrained`,
    `from_config` or within the `apply_patches` context manager.

    Use this to register class replacements that will be automatically applied when loading any model.
    This is useful for quantization library compatibility, structural optimizations, and architectural
    experimentation. The mapping is global, can grow with multiple calls, and can be cleared entirely.

    Args:
        mapping (`Dict[str, type[nn.Module]]`):
            Mapping from original class names (or regex patterns) to replacement classes. Supports:
            - Exact class names: `"Qwen2MoeExperts"` → `CustomExperts`
            - Regex patterns: `".*Attention"` matches `LlamaAttention`, `MistralAttention`, etc.,
            or `"^Llama\\d+Attention$"` matches `Llama2Attention`, `Llama3Attention`, etc.

            Exact matches take precedence over patterns. Patterns are matched using `re.search()`,
            so they can match anywhere in the class name unless you use anchors (`^` for start, `$` for end).
        overwrite (`bool`, *optional*, defaults to `False`):
            Whether to overwrite existing mappings for class names that are already registered.

    Example:
        ```python
        from transformers import AutoModelForCausalLM
        from transformers.monkey_patching import register_patch_mapping

        # Define custom expert implementation
        class SequentialExperts(nn.Module):
            ...

        # Register exact class name
        register_patch_mapping(
            mapping={"Qwen2MoeExperts": SequentialExperts}
        )

        # Register with regex pattern to match multiple classes
        register_patch_mapping(
            mapping={".*Attention": CustomAttention}  # Matches LlamaAttention, MistralAttention, etc.
        )

        # Match specific model versions
        register_patch_mapping(
            mapping={"^Llama\\d+Attention$": CustomLlamaAttention}  # Matches Llama2Attention, Llama3Attention
        )

        # The patch will be automatically applied during loading
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
        ```

    Note:
        For weight conversions, use [`~transformers.register_checkpoint_conversion_mapping`] instead.
    """
    global _monkey_patch_mapping_cache
    with _monkey_patch_lock:
        for class_name, replacement_class in mapping.items():
            # Validate that replacement_class is actually a class and is a subclass of nn.Module
            if not isinstance(replacement_class, type):
                raise TypeError(
                    f"Replacement for '{class_name}' must be a class, got {type(replacement_class).__name__}"
                )
            if not issubclass(replacement_class, nn.Module):
                raise TypeError(
                    f"Replacement class for '{class_name}' must be a subclass of nn.Module, "
                    f"got {replacement_class.__name__} which inherits from {[c.__name__ for c in replacement_class.__mro__[1:]]}"
                )

            if class_name in _monkey_patch_mapping_cache and not overwrite:
                raise ValueError(
                    f"Class '{class_name}' already has a patch mapping registered. Use overwrite=True to replace it."
                )
            _monkey_patch_mapping_cache[class_name] = replacement_class

