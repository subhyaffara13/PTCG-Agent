
def set_per_process_memory_fraction(fraction, device: "Device" = None) -> None:
    r"""Set memory fraction for a process.

    The fraction is used to limit an caching allocator to allocated memory on a CUDA device.
    The allowed value equals the total visible memory multiplied fraction.
    If trying to allocate more than the allowed value in a process, will raise an out of
    memory error in allocator.

    Args:
        fraction(float): Range: 0~1. Allowed memory equals total_memory * fraction.
        device (torch.device or int, optional): selected device. If it is
            ``None`` the default CUDA device is used.
    .. note::
        In general, the total available free memory is less than the total capacity.
    """
    _lazy_init()
    if device is None:
        device = torch.cuda.current_device()
    device = _get_device_index(device)
    if not isinstance(fraction, float):
        raise TypeError("Invalid type for fraction argument, must be `float`")
    if fraction < 0 or fraction > 1:
        raise ValueError(f"Invalid fraction value: {fraction}. Allowed range: 0~1")

    torch._C._cuda_setMemoryFraction(fraction, device)


def set_per_process_memory_fraction(fraction) -> None:
    r"""Set memory fraction for limiting process's memory allocation on MPS device.
    The allowed value equals the fraction multiplied by recommended maximum device memory
    (obtained from Metal API device.recommendedMaxWorkingSetSize).
    If trying to allocate more than the allowed value in a process, it will raise an out of
    memory error in allocator.

    Args:
        fraction(float): Range: 0~2. Allowed memory equals total_memory * fraction.

    .. note::
       Passing 0 to fraction means unlimited allocations
       (may cause system failure if out of memory).
       Passing fraction greater than 1.0 allows limits beyond the value
       returned from device.recommendedMaxWorkingSetSize.
    """

    if not isinstance(fraction, float):
        raise TypeError("Invalid type for fraction argument, must be `float`")
    if fraction < 0 or fraction > 2:
        raise ValueError(f"Invalid fraction value: {fraction}. Allowed range: 0~2")

    torch._C._mps_setMemoryFraction(fraction)


def set_per_process_memory_fraction(fraction: float, device: Device = None) -> None:
    r"""
    Set the memory fraction for a single process on XPU device.
    This function limits the amount of memory that the caching allocator can allocate
    on the specified XPU device. The allowed memory is computed as:

    .. math:: \text{allowed\_memory} = \text{total\_memory} \times \text{fraction}

    If the process attempts to allocate more than this allowed memory,
    an out-of-memory error will be raised by the allocator.

    Arguments:
        fraction (float): Range: 0~1. Allowed memory equals total_memory * fraction.
        device (torch.device or int or str, optional): selected device. It uses the current device,
            given by :func:`~torch.xpu.current_device`, if :attr:`device` is ``None`` (default).

    .. note:: In general, the total available free memory is less than the total capacity.
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    if not isinstance(fraction, float):
        raise TypeError("Invalid type for fraction argument, must be `float`")
    torch._C._xpu_setMemoryFraction(fraction, device)

