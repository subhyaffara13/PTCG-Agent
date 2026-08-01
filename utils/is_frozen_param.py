
def is_frozen_param(t: torch.Tensor) -> bool:
    """
    Return True if the tensor is a frozen param.
    """
    return getattr(t, "_is_frozen_param", False)

