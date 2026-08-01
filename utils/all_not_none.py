
def all_not_none(*args) -> bool:
    """
    Returns a boolean indicating if all arguments are not None.
    """
    return all(arg is not None for arg in args)

