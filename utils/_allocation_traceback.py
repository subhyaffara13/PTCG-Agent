
def _allocation_traceback(data_ptr: int) -> list[dict[str, Any]] | None:
    r"""Return the allocation traceback for a currently-allocated CUDA pointer,
    or ``None`` if the pointer is not found or recording was not enabled.

    ``data_ptr`` must be the base address of a recorded allocation, e.g. the
    result of ``tensor.untyped_storage().data_ptr()``. Passing the result of
    ``tensor.data_ptr()`` for a view with a nonzero ``storage_offset`` may
    return ``None`` even if the underlying allocation is still live.

    Requires :func:`_record_memory_history` to have been called with
    ``context != None`` beforehand.
    """
    return torch._C._cuda_allocationTraceback(data_ptr)

