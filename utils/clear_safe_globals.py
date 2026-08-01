
def clear_safe_globals() -> None:
    """
    Clears the list of globals that are safe for ``weights_only`` load.
    """
    _weights_only_unpickler._clear_safe_globals()

