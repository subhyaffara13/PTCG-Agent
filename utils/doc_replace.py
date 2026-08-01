
def doc_replace(obj: object, oldval: str, newval: str) -> Decorator:
    """Decorator to take the docstring from obj, with oldval replaced by newval

    Equivalent to ``func.__doc__ = obj.__doc__.replace(oldval, newval)``

    Parameters
    ----------
    obj : object
        A class or object whose docstring will be used as the basis for the
        replacement operation.
    oldval : str
        The string to search for in the docstring.
    newval : str
        The string to replace `oldval` with in the docstring.

    Returns
    -------
    decfunc : function
        A decorator function that replaces occurrences of `oldval` with `newval`
        in the docstring of the decorated function.
    """
    # __doc__ may be None for optimized Python (-OO)
    doc = (obj.__doc__ or "").replace(oldval, newval)

    def inner(func: _F) -> _F:
        func.__doc__ = doc
        return func

    return inner

