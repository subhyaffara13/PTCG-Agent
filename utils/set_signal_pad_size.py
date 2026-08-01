
def set_signal_pad_size(size: int) -> None:
    r"""
    Set the signal pad size for future symmetric memory allocations.

    Signal pads are P2P-accessible memory regions used for synchronization in
    symmetric memory. This function allows users to configure
    the signal pad size to be proportional to their workload requirements.

    .. warning::
        This must be called before any symmetric memory allocations are made.
        The size cannot be changed after allocations have been performed.

    Args:
        size (int): the signal pad size in bytes. The size should be
            proportional to the number of blocks launched and the world size.

    Example::

        >>> # doctest: +SKIP
        >>> # Set a larger signal pad size before any allocations
        >>> torch.distributed._symmetric_memory.set_signal_pad_size(1024 * 1024)  # 1MB
    """
    _SymmetricMemory.signal_pad_size = size

