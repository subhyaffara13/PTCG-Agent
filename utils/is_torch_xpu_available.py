
def is_torch_xpu_available(check_device: bool = False) -> bool:
    """
    Checks if XPU acceleration is available via stock PyTorch (>=2.6) and
    potentially if a XPU is in the environment.
    """
    if not is_torch_available():
        return False

    torch_version = version.parse(get_torch_version())
    if torch_version.major == 2 and torch_version.minor < 6:
        return False

    import torch

    if check_device:
        try:
            # Will raise a RuntimeError if no XPU is found
            _ = torch.xpu.device_count()
            return torch.xpu.is_available()
        except RuntimeError:
            return False
    return hasattr(torch, "xpu") and torch.xpu.is_available()

