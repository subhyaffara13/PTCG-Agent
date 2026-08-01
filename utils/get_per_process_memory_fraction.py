
def get_per_process_memory_fraction(device: "Device" = None) -> float:
    r"""Get memory fraction for a process.

    Args:
        device (torch.device or int, optional): selected device. If it is
            ``None`` the default CUDA device is used.
    Returns:
        memory fraction, in range 0~1. Allowed memory equals total_memory * fraction.
    """
    _lazy_init()
    if device is None:
        device = torch.cuda.current_device()
    device = _get_device_index(device)
    return torch._C._cuda_getMemoryFraction(device)


def get_per_process_memory_fraction(device: Device = None) -> float:
    r"""
    Retrieve the memory fraction currently set for a process on a given XPU device.
    This fraction represents the portion of the total device memory that
    the caching allocator is allowed to use. The allowed memory is calculated as:

    .. math:: \text{allowed\_memory} = \text{total\_memory} \times \text{fraction}

    Args:
        device (torch.device or int or str, optional): selected device. It uses the current device,
            given by :func:`~torch.xpu.current_device`, if :attr:`device` is ``None`` (default).

    Returns:
        float: The memory fraction in the range 0.0 to 1.0.
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_getMemoryFraction(device)

