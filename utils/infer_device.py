
def infer_device(model):
    """
    Infers the device type from the model parameters.
    Args:
        model: The model instance.

    Returns:
        The device type.
    """
    EXAMPLE_MAPPING = """
    {
        "RMSNorm": {
            "cuda":
                "kernels-community/layer_norm:LlamaRMSNorm",
            ...
        },
        ...
    }
    """
    try:
        param = next(model.parameters())
    except StopIteration:
        raise ValueError(
            f"Cannot determine model device, please provide a device to the mapping. Example: {EXAMPLE_MAPPING}"
        )

    dev_type = param.device.type
    if dev_type == "cuda":
        # Refine based on actual platform
        from ..utils import is_torch_available

        if is_torch_available():
            import torch

            if getattr(torch, "version").hip is not None:
                return "rocm"

    return dev_type

