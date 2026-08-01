
def register_checkpoint_conversion_mapping(
    model_type_or_class_name: str,
    mapping: list[WeightConverter | WeightRenaming],
    overwrite: bool = False,
) -> None:
    """
    Register a conversion mapping for a model type string or a class name.

    Class names take priority over `model_type` strings during lookup (see
    `extract_weight_conversions_for_model`), making it possible to define
    task-head-specific or class-specific conversions that differ from the shared
    `model_type` baseline.
    """
    global _checkpoint_conversion_mapping_cache
    if _checkpoint_conversion_mapping_cache is None:
        _checkpoint_conversion_mapping_cache = _build_checkpoint_conversion_mapping()
    if model_type_or_class_name in _checkpoint_conversion_mapping_cache and not overwrite:
        raise ValueError(
            f"Conversion mapping for '{model_type_or_class_name}' already exists. Pass overwrite=True to replace it."
        )
    _checkpoint_conversion_mapping_cache[model_type_or_class_name] = mapping

