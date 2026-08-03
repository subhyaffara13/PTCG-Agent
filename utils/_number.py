from typing import Union

def _number(s: Union[str, int, float]) -> IntFloat:
    """
    Given a numeric string, return an integer or a float, whichever
    the string indicates. _number("1") will return the integer 1,
    _number("1.0") will return the float 1.0.

    >>> _number("1")
    1
    >>> _number("1.0")
    1.0
    >>> _number("a")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    GlifLibError: Could not convert a to an int or float.
    """
    try:
        n: IntFloat = int(s)
        return n
    except ValueError:
        pass
    try:
        n = float(s)
        return n
    except ValueError:
        raise GlifLibError("Could not convert %s to an int or float." % s)

