
def current_process_group() -> ProcessGroup:
    """
    Get the current process group. Thread local method.

    Returns:
        The current process group.
    """
    return _current_process_group()

