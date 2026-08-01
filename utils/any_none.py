
def any_none(*args) -> bool:
    """
    Returns a boolean indicating if any argument is None.
    """
    return any(arg is None for arg in args)

