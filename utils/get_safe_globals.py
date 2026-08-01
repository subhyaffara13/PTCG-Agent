
def get_safe_globals() -> list[Callable | tuple[Callable, str]]:
    """
    Returns the list of user-added globals that are safe for ``weights_only`` load.
    """
    return _weights_only_unpickler._get_safe_globals()

