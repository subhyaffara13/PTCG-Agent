
def get_memory_info(device_index: _device_t = None, /) -> tuple[int, int]:
    r"""Return the current device memory information for a given device index.

    Args:
        device_index (:class:`torch.device`, str, int, optional): the index of the device to target.
            If not given, use :func:`torch.accelerator.current_device_index` by default.
            If a :class:`torch.device` or str is provided, its type must match the current
            :ref:`accelerator<accelerators>` device type.

    Returns:
        tuple[int, int]: a tuple of two integers (free_memory, total_memory) in bytes.
            The first value is the free memory on the device (available across all processes and applications),
            The second value is the device's total hardware memory capacity.
    """
    device_index = _get_device_index(device_index, optional=True)
    # pyrefly: ignore [missing-attribute]
    return torch._C._accelerator_getMemoryInfo(device_index)

