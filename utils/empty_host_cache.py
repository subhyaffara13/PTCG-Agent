
def empty_host_cache() -> None:
    r"""Release all unoccupied cached host (pinned) memory currently held by the host caching
    allocator so that it can be used by other applications.

    .. note:: This function is a no-op if the memory allocator for the current
        :ref:`accelerator <accelerators>` has not been initialized.
    """
    torch._C._accelerator_emptyHostCache()

