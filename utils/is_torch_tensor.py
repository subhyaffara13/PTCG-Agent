
def is_torch_tensor(x) -> bool:
    """
    Tests if `x` is a torch tensor or not. Safe to call even if torch is not installed.
    """
    if not _is_torch_available:
        return False

    import torch

    return isinstance(x, torch.Tensor)

