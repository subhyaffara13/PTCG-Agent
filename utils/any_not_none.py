
def any_not_none(*args) -> bool:
    """
    Returns a boolean indicating if any argument is not None.
    """
    return any(arg is not None for arg in args)

