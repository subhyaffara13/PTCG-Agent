
def get_mem_pool(device: _device) -> torch.cuda.MemPool:
    """
    Get the symmetric memory pool for a given device. If not found, create a new
    pool.

    The tensor allocations with this pool must be symmetric across ranks.  The
    allocated tensors can be used with symmetric operations, for example,
    operations defined under `torch.ops.symm_mem`.

    Args:
        device (`torch.device` or str): the device for which to get the symmetric memory pool.

    Returns:
        `torch.cuda.MemPool`: the symmetric memory pool for the given device.

    Example::

        >>> # doctest: +SKIP
        >>> pool = torch.distributed._symmetric_memory.get_mem_pool("cuda:0")
        >>> with torch.cuda.use_mem_pool(pool):
        >>>     tensor = torch.randn(1000, device="cuda:0")
        >>> tensor = torch.ops.symm_mem.one_shot_all_reduce(tensor, "sum", group_name)

    """
    # This function is a wrapper around the `torch.cuda.MemPool` constructor.
    # Due to special requirements of SymmetricMemory, we preset certain options for the pool.
    # - use_on_oom=False: we don't want to lend the space of the pool for
    # non-symmetric allocations because this could desync the allocation state
    # across ranks.
    # - no_split=True: we don't want to split segments, because today a segment
    # is associated with a signal pad, if two allocated tensors share a segment
    # and their kernels concurrently use (the same) signal pad, this could cause
    # undefined behaviors. We could consider relaxing this in the future if we
    # establish stream tracking and implicit synchronization around an
    # allocation.
    if device not in _symm_mem_pools:
        allocator = get_mempool_allocator(device)
        # Create a new pool with the given allocator and the preset options.
        _symm_mem_pools[device] = torch.cuda.MemPool(
            allocator,
            use_on_oom=False,
            no_split=True,
        )

    return _symm_mem_pools[device]

