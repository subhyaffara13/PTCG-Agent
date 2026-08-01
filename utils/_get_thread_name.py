
def _get_thread_name() -> str:
    """Get the name of the current thread.

    Returns:
        str: Name of the current thread.
    """
    return torch._C._get_thread_name()

