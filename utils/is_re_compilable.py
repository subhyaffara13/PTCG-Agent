import re

def is_re_compilable(obj: object) -> bool:
    """
    Check if the object can be compiled into a regex pattern instance.

    Parameters
    ----------
    obj : The object to check
        The object to check if the object can be compiled into a regex pattern instance.

    Returns
    -------
    bool
        Whether `obj` can be compiled as a regex pattern.

    See Also
    --------
    api.types.is_re : Check if the object is a regex pattern instance.

    Examples
    --------
    >>> from pandas.api.types import is_re_compilable
    >>> is_re_compilable(".*")
    True
    >>> is_re_compilable(1)
    False
    """
    try:
        re.compile(obj)  # type: ignore[call-overload]
    except TypeError:
        return False
    else:
        return True

