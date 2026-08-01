
def reset_peak_memory_stats(device_index: _device_t = None, /) -> None:
    r"""Reset the "peak" stats tracked by the current :ref:`accelerator<accelerators>`
    memory allocator for a given device index.

    Args:
        device_index (:class:`torch.device`, str, int, optional): the index of the device to target.
            If not given, use :func:`torch.accelerator.current_device_index` by default.
            If a :class:`torch.device` or str is provided, its type must match the current
            :ref:`accelerator<accelerators>` device type.

    .. note:: This function is a no-op if the memory allocator for the current
        :ref:`accelerator <accelerators>` has not been initialized.
    """
    device_index = _get_device_index(device_index, optional=True)
    return torch._C._accelerator_resetPeakStats(device_index)


def reset_peak_memory_stats(device: "Device" = None) -> None:
    r"""Reset the "peak" stats tracked by the CUDA memory allocator.

    See :func:`~torch.cuda.memory_stats` for details. Peak stats correspond to the
    `"peak"` key in each individual stat dict.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        See :ref:`cuda-memory-management` for more details about GPU memory
        management.
    """
    device = _get_device_index(device, optional=True)
    return torch._C._cuda_resetPeakMemoryStats(device)


def reset_peak_memory_stats(device: Device = None) -> None:
    r"""Reset the peak memory stats for a given device.


    Args:
        device (torch.device, str, or int, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).
    """
    if not is_initialized():
        return
    torch._C._mtia_resetPeakMemoryStats(_get_device_index(device, optional=True))


def reset_peak_memory_stats(device: Device = None) -> None:
    r"""Reset the "peak" stats tracked by the XPU memory allocator.

    See :func:`~torch.xpu.memory_stats` for details. Peak stats correspond to the
    `"peak"` key in each individual stat dict.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_resetPeakMemoryStats(device)

