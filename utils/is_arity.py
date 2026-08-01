
def is_arity(n, func, sigspec=None):
    """ Does a function have only n positional arguments?

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def f(x):
    ...     return x
    >>> is_arity(1, f)
    True
    >>> def g(x, y=1):
    ...     return x + y
    >>> is_arity(1, g)
    False
    """
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._is_arity, n, func)
    if sigspec is None:
        return rv
    num = num_required_args(func, sigspec)
    if num is not None:
        num = num == n
        if not num:
            return False
    varargs = has_varargs(func, sigspec)
    if varargs:
        return False
    keywords = has_keywords(func, sigspec)
    if keywords:
        return False
    if num is None or varargs is None or keywords is None:  # pragma: no cover
        return None
    return True

