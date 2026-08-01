
def _set_thread_name(name: str) -> None:
    """Set the name of the current thread.

    Args:
        name (str): Name of the current thread.
    """
    torch._C._set_thread_name(name)

