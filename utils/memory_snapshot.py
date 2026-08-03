from typing import Any

def memory_snapshot(mempool_id=None, include_traces=True):
    r"""Return a snapshot of the CUDA memory allocator state across all devices.

    Interpreting the output of this function requires familiarity with the
    memory allocator internals.

    Args:
        mempool_id: Optional memory pool ID to get snapshot for a specific pool
        include_traces: Whether to include trace entries in the snapshot.
            If True (default), all trace entries are included.
            If False, no trace entries are included (lightweight/fast snapshot).

    .. note::
        See :ref:`cuda-memory-management` for more details about GPU memory
        management.
    """
    if mempool_id is None:
        # pyrefly: ignore [bad-argument-type]
        return torch._C._cuda_memorySnapshot((0, 0, include_traces))["segments"]
    else:
        return torch._C._cuda_memorySnapshot(
            # pyrefly: ignore [bad-argument-type]
            (mempool_id[0], mempool_id[1], include_traces)
        )["segments"]


def memory_snapshot(
    mempool_id: tuple[int, int] | None = None,
) -> list[dict[str, Any]]:
    r"""
    Return a snapshot of the XPU memory allocator state across all devices.
    Provides detailed information for each memory segment managed by the allocator
    including its size, owning pool, associated stream, call stack traces, and other relevant attributes.

    Arguments:
        mempool_id (tuple[int, int] or None, optional): The memory pool id. If None, the default memory pool is used.

    Returns:
        list[dict[str, Any]]: List of memory segments and their attributes.
    """
    if not is_initialized():
        return []
    return torch._C._xpu_memorySnapshot(mempool_id)["segments"]

