
def layer_type_validation(layer_types: list[str], num_hidden_layers: int | None = None, attention: bool = True):
    logger.warning(
        "`layer_type_validation` is deprecated and will be removed in v5.20. "
        "Use `PreTrainedConfig.validate_layer_type` instead"
    )

    if not all(layer_type in ALLOWED_LAYER_TYPES for layer_type in layer_types):
        raise ValueError(f"The `layer_types` entries must be in {ALLOWED_LAYER_TYPES}")
    if num_hidden_layers is not None and num_hidden_layers != len(layer_types):
        raise ValueError(
            f"`num_hidden_layers` ({num_hidden_layers}) must be equal to the number of layer types "
            f"({len(layer_types)})"
        )

