
def is_torch_device(x) -> bool:
    """
    Tests if `x` is a torch device or not. Safe to call even if torch is not installed.
    """
    if not _is_torch_available:
        return False

    import torch

    return isinstance(x, torch.device)

