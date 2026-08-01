
def change_current_allocator(allocator: _CUDAAllocator) -> None:
    r"""Change the currently used memory allocator to be the one provided.

    If the current allocator has already been used/initialized, this function will error.


    Args:
        allocator (torch.cuda.memory._CUDAAllocator): allocator to be set as the active one.
    .. note::
        See :ref:`cuda-memory-management` for details on creating and using a custom allocator
    """
    torch._C._cuda_changeCurrentAllocator(allocator.allocator())


def change_current_allocator(allocator: _XPUAllocator) -> None:
    r"""Change the currently used memory allocator to be the one provided.

    .. note::
        If the current allocator has already been used/initialized, this function will error.

    Arguments:
        allocator (torch.xpu.memory._XPUAllocator): allocator to be set as the active one.
    """
    torch._C._xpu_changeCurrentAllocator(allocator.allocator())

