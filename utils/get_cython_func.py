
def get_cython_func(arg: Callable) -> str | None:
    """
    if we define an internal function for this argument, return it
    """
    return _cython_table.get(arg)

