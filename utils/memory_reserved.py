
def memory_reserved(device_index: _device_t = None, /) -> int:
    r"""Return the current :ref:`accelerator<accelerators>` device memory managed by the caching allocator
    in bytes for a given device index.

    Args:
        device_index (:class:`torch.device`, str, int, optional): the index of the device to target.
            If not given, use :func:`torch.accelerator.current_device_index` by default.
            If a :class:`torch.device` or str is provided, its type must match the current
            :ref:`accelerator<accelerators>` device type.

    Returns:
        int: the current memory reserved by PyTorch (in bytes) within the current process.
    """
    return memory_stats(device_index).get("reserved_bytes.all.current", 0)


def memory_reserved(device: "Device" = None) -> int:
    r"""Return the current GPU memory managed by the caching allocator in bytes for a given device.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        See :ref:`cuda-memory-management` for more details about GPU memory
        management.
    """
    return memory_stats(device=device).get("reserved_bytes.all.current", 0)


def memory_reserved(device: Device = None) -> int:
    r"""Return the current GPU memory managed by the caching allocator in bytes for a given device.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    return memory_stats(device=device).get("reserved_bytes.all.current", 0)

