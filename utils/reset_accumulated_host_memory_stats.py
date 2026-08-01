
def reset_accumulated_host_memory_stats() -> None:
    r"""Reset the "accumulated" (historical) stats tracked by the host memory allocator.

    See :func:`~torch.cuda.host_memory_stats` for details. Accumulated stats correspond to
    the `"allocated"` and `"freed"` keys in each individual stat dict.
    """
    return torch._C._cuda_resetAccumulatedHostMemoryStats()

