
def empty_cache() -> None:
    r"""Release all unoccupied cached memory currently held by the caching
    allocator so that those can be used in other application.

    .. note:: This function is a no-op if the memory allocator for the current
        :ref:`accelerator <accelerators>` has not been initialized.
    """
    if not torch._C._accelerator_isAllocatorInitialized():
        return
    torch._C._accelerator_emptyCache()


def empty_cache() -> None:
    r"""Release all unoccupied cached memory currently held by the caching
    allocator so that those can be used in other GPU application and visible in
    `nvidia-smi`.

    .. note::
        :func:`~torch.cuda.empty_cache` doesn't increase the amount of GPU
        memory available for PyTorch. However, it may help reduce fragmentation
        of GPU memory in certain cases. See :ref:`cuda-memory-management` for
        more details about GPU memory management.
    """
    if is_initialized():
        torch._C._cuda_emptyCache()


def empty_cache() -> None:
    r"""Releases all unoccupied cached memory currently held by the caching
    allocator so that those can be used in other GPU applications.
    """
    torch._C._mps_emptyCache()


def empty_cache() -> None:
    r"""Empty the MTIA device cache."""
    return torch._C._mtia_emptyCache()


def empty_cache() -> None:
    r"""Release all unoccupied cached memory currently held by the caching
    allocator so that those can be used in other XPU application.

    .. note::
        :func:`~torch.xpu.empty_cache` doesn't increase the amount of XPU
        memory available for PyTorch. However, it may help reduce fragmentation
        of XPU memory in certain cases.
    """
    if is_initialized():
        torch._C._xpu_emptyCache()

