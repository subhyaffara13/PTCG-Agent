
def get_allocator_backend() -> str:
    r"""Return a string describing the active allocator backend as set by
    ``PYTORCH_ALLOC_CONF``. Currently available backends are
    ``native`` (PyTorch's native caching allocator) and `cudaMallocAsync``
    (CUDA's built-in asynchronous allocator).

    .. note::
        See :ref:`cuda-memory-management` for details on choosing the allocator backend.
    """
    return torch._C._cuda_getAllocatorBackend()

