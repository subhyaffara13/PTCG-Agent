
def extract_weight_conversions_for_model(
    model: PreTrainedModel,
) -> list[WeightTransform] | None:
    """
    Return the registered conversion list for `model`, or `None` if none exists.

    Looks up by class name first (enables task-head-specific overrides), then
    falls back to `model.config.model_type`.  Transforms are returned
    unmodified; the caller sets `scope_prefix` on each transform for sub-module isolation.
    """
    class_name = type(model).__name__
    model_type = model.config.model_type

    # Class name takes priority — allows ForXxx-specific overrides
    conversions = get_checkpoint_conversion_mapping(class_name)
    if conversions is None and model_type:
        conversions = get_checkpoint_conversion_mapping(model_type)
    return conversions

