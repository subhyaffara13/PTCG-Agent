
def all_none(*args) -> bool:
    """
    Returns a boolean indicating if all arguments are None.
    """
    return all(arg is None for arg in args)


def allNone(lst):
    return all(l is None for l in lst)

