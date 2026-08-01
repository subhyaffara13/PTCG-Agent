
def is_terminal() -> bool:
    """
    Detect if Python is running in a terminal.

    Returns True if Python is running in a terminal or False if not.
    """
    try:
        # error: Name 'get_ipython' is not defined
        ip = get_ipython()  # type: ignore[name-defined]
    except NameError:  # assume standard Python interpreter in a terminal
        return True
    else:
        if hasattr(ip, "kernel"):  # IPython as a Jupyter kernel
            return False
        else:  # IPython in a terminal
            return True

