
def reset_peak_host_memory_stats() -> None:
    r"""Reset the "peak" stats tracked by the host memory allocator.

    See :func:`~torch.cuda.host_memory_stats` for details. Peak stats correspond to the
    `"peak"` key in each individual stat dict.
    """
    return torch._C._cuda_resetPeakHostMemoryStats()

