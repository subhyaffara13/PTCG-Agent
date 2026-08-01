
def get_signal_pad_size() -> int:
    r"""
    Get the current signal pad size for symmetric memory allocations.

    Returns the user-configured size if set via :func:`set_signal_pad_size`,
    otherwise returns the default size.

    Returns:
        int: the signal pad size in bytes.

    Example::

        >>> # doctest: +SKIP
        >>> size = torch.distributed._symmetric_memory.get_signal_pad_size()
        >>> print(f"Signal pad size: {size} bytes")
    """
    return _SymmetricMemory.signal_pad_size

