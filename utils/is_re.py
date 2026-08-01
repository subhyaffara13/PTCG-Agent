
def is_re(obj: object) -> TypeGuard[Pattern]:
    """
    Check if the object is a regex pattern instance.

    Parameters
    ----------
    obj : object
        The object to check for being a regex pattern. Typically,
        this would be an object that you expect to be a compiled
        pattern from the `re` module.

    Returns
    -------
    bool
        Whether `obj` is a regex pattern.

    See Also
    --------
    api.types.is_float : Return True if given object is float.
    api.types.is_iterator : Check if the object is an iterator.
    api.types.is_integer : Return True if given object is integer.
    api.types.is_re_compilable : Check if the object can be compiled
                                into a regex pattern instance.

    Examples
    --------
    >>> from pandas.api.types import is_re
    >>> import re
    >>> is_re(re.compile(".*"))
    True
    >>> is_re("foo")
    False
    """
    return isinstance(obj, Pattern)

