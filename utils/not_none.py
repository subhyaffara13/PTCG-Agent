
def not_none(obj: T | None) -> T:
    if obj is None:
        raise TypeError("Invariant encountered: value was None when it should not be")
    return obj


def not_none(*args):
    """
    Returns a generator consisting of the arguments that are not None.
    """
    return (arg for arg in args if arg is not None)

