
def isiterable(x):
    """ Is x iterable?

    >>> isiterable([1, 2, 3])
    True
    >>> isiterable('abc')
    True
    >>> isiterable(5)
    False
    """
    try:
        iter(x)
        return True
    except TypeError:
        return False


def isiterable(obj: object) -> TypeGuard[collections.abc.Iterable[object]]:
    try:
        iter(obj)  # type: ignore[call-overload]
        return not istext(obj)
    except Exception:
        return False

