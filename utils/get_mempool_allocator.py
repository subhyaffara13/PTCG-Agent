
def get_mempool_allocator(device: _device):  # type: ignore[no-untyped-def]
    r"""
    Get the MemPool allocator for symmetric memory for a given device.

    Args:
        device (`torch.device` or str): the device for which to get the MemPool
            allocator.
    """
    return _SymmetricMemory.get_mempool_allocator(torch.device(device))

