
def _validate_int(n, bound, name):
    msg = f'{name} must be an integer not less than {bound}, but got {n!r}'
    try:
        n = operator.index(n)
    except TypeError:
        raise TypeError(msg) from None
    if n < bound:
        raise ValueError(msg)
    return n


def _validate_int(k, name, minimum=None):
    """
    Validate a scalar integer.

    This function can be used to validate an argument to a function
    that expects the value to be an integer.  It uses `operator.index`
    to validate the value (so, for example, k=2.0 results in a
    TypeError).

    Parameters
    ----------
    k : int
        The value to be validated.
    name : str
        The name of the parameter.
    minimum : int, optional
        An optional lower bound.
    """
    try:
        k = operator.index(k)
    except TypeError:
        raise TypeError(f'{name} must be an integer.') from None
    if minimum is not None and k < minimum:
        raise ValueError(f'{name} must be an integer not less '
                         f'than {minimum}') from None
    return k

