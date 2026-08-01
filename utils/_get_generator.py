
def _get_generator(device: torch.device) -> torch._C.Generator:
    r"""Return the CUDA Generator object for the given device.

    Args:
        device (torch.device): selected device.
    """
    idx = device.index
    if idx is None:
        idx = current_device()
    return torch.cuda.default_generators[idx]


def _get_generator(device: torch.device) -> torch._C.Generator:
    r"""Return the XPU Generator object for the given device.

    Args:
        device (torch.device): selected device.
    """
    idx = device.index
    if idx is None:
        idx = current_device()
    return torch.xpu.default_generators[idx]

