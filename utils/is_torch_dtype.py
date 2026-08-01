
def is_torch_dtype(x) -> bool:
    """
    Tests if `x` is a torch dtype or not. Safe to call even if torch is not installed.
    """
    if not _is_torch_available:
        return False

    import torch

    if isinstance(x, str):
        if hasattr(torch, x):
            x = getattr(torch, x)
        else:
            return False
    return isinstance(x, torch.dtype)

