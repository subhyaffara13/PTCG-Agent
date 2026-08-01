
def use_mem_pool(pool: MemPool, device: "Device" = None):
    r"""A context manager that routes allocations to a given pool.

    Args:
        pool(torch.cuda.MemPool): a MemPool object to be made active so that
            allocations route to this pool.
        device (torch.device or int, optional): selected device. Uses MemPool on
            the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        This context manager makes only current thread's allocations route to
        the given pool. If a new thread is spawned inside the context manager
        (e.g. by calling backward) the allocations in that thread will not
        route to the given pool.
    """
    device_index = (
        torch.cuda.current_device() if device is None else _get_device_index(device)
    )
    _cuda_beginAllocateCurrentThreadToPool(device_index, pool.id)
    try:
        yield
    finally:
        _cuda_endAllocateToPool(device_index, pool.id)
        _cuda_releasePool(device_index, pool.id)


def use_mem_pool(pool: MemPool, device: "Device" = None):
    r"""A context manager that routes allocations to a given pool.

    Args:
        pool(torch.xpu.MemPool): a :class:`MemPool` object to be made active so that
            allocations route to this pool.
        device (torch.device or int, optional): selected device. Uses :class:`MemPool on
            the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        This context manager makes only current thread's allocations route to
        the given pool. If a new thread is spawned inside the context manager
        (e.g. by calling backward) the allocations in that thread will not
        route to the given pool.
    """
    device_index = (
        torch.xpu.current_device() if device is None else _get_device_index(device)
    )
    torch._C._xpu_beginAllocateCurrentThreadToPool(device_index, pool.id)
    try:
        yield
    finally:
        torch._C._xpu_endAllocateToPool(device_index, pool.id)
        torch._C._xpu_releasePool(device_index, pool.id)

