
def mem_get_info(device: "Device" = None) -> tuple[int, int]:
    r"""Return the global free and total GPU memory for a given device using cudaMemGetInfo.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default) or if the device index is not specified.

    .. note::
        See :ref:`cuda-memory-management` for more
        details about GPU memory management.
    """
    if device is None:
        device = torch.cuda.current_device()
    # optional=True allows `device = torch.device('cuda')` for which device.index is None
    device = _get_device_index(device, optional=True)
    return torch.cuda.cudart().cudaMemGetInfo(device)


def mem_get_info(device: Device = None) -> tuple[int, int]:
    r"""Return the global free and total GPU memory for a given device.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).

    Returns:
        tuple[int, int]: a tuple of two integers (free_memory, total_memory) in bytes.
            The first value is the free memory on the device (available across all processes and applications),
            The second value is the device's total hardware memory capacity.
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_getMemoryInfo(device)

