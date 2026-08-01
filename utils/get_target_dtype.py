
def get_target_dtype(query: torch.Tensor, module: torch.nn.Module) -> torch.dtype:
    """If the query is in float32, return a target dtype compatible with flash attention. Return None otherwise."""
    if query.dtype == torch.float32:
        device_type = query.device.type
        if torch.is_autocast_enabled(device_type):
            return torch.get_autocast_dtype(device_type)
        # Handle the case where the model is quantized
        elif hasattr(module.config, "_is_quantized"):
            return module.config.dtype
        else:
            return next(layer for layer in module.modules() if isinstance(layer, torch.nn.Linear)).weight.dtype
    return None

