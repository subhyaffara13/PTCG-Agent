
def synchronize(device: _device_t = None, /) -> None:
    r"""Wait for all kernels in all streams on the given device to complete.

    Args:
        device (:class:`torch.device`, str, int, optional): device for which to synchronize. It must match
            the current :ref:`accelerator<accelerators>` device type. If not given,
            use :func:`torch.accelerator.current_device_index` by default.

    .. note:: This function is a no-op if the current :ref:`accelerator<accelerators>` is not initialized.

    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CUDA)
        >>> assert torch.accelerator.is_available() "No available accelerators detected."
        >>> start_event = torch.Event(enable_timing=True)
        >>> end_event = torch.Event(enable_timing=True)
        >>> start_event.record()
        >>> tensor = torch.randn(100, device=torch.accelerator.current_accelerator())
        >>> sum = torch.sum(tensor)
        >>> end_event.record()
        >>> torch.accelerator.synchronize()
        >>> elapsed_time_ms = start_event.elapsed_time(end_event)
    """
    device_index = _get_device_index(device, optional=True)
    torch._C._accelerator_synchronizeDevice(device_index)


def synchronize(device: torch.types.Device = None) -> None:
    r"""Waits for all kernels in all streams on the CPU device to complete.

    Args:
        device (torch.device or int, optional): ignored, there's only one CPU device.

    N.B. This function only exists to facilitate device-agnostic code.
    """


def synchronize(device: Device = None) -> None:
    r"""Wait for all kernels in all streams on a CUDA device to complete.

    Args:
        device (torch.device or int, optional): device for which to synchronize.
            It uses the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    _lazy_init()
    with torch.cuda.device(device):
        return torch._C._cuda_synchronize()


def synchronize() -> None:
    r"""Waits for all kernels in all streams on a MPS device to complete."""
    return torch._C._mps_deviceSynchronize()


def synchronize(device: Device = None) -> None:
    r"""Waits for all jobs in all streams on a MTIA device to complete."""
    with torch.mtia.device(device):
        return torch._C._mtia_deviceSynchronize()


def synchronize(device: Device = None) -> None:
    r"""Wait for all kernels in all streams on a XPU device to complete.

    Args:
        device (torch.device or int, optional): device for which to synchronize.
            It uses the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_synchronize(device)


def synchronize() -> None:
    pass


def synchronize(device: str = "cuda") -> None:
    if device == "cpu":
        return
    device_interface = get_interface_for_device(device)
    if device_interface.is_available():
        device_interface.synchronize()


def synchronize(
    store,
    data: bytes,
    rank: int,
    world_size: int,
    key_prefix: str,
    timeout: float = 300,
) -> list[bytes]:
    """
    Synchronizes ``world_size`` agents between each other using the underlying c10d store.
    The ``data`` will be available on each of the agents.

    Note: The data on the path is not deleted, as a result there can be stale data if
        you use the same key_prefix twice.

    Time complexity: O(N) per worker, O(N^2) globally.
    """
    with store_timeout(store, timeout):
        store.set(f"{key_prefix}{rank}", data)
        agent_data = get_all(store, rank, key_prefix, world_size)
        return agent_data

