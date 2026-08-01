
def _iterable_of_int(x, name=None):
    """Convert ``x`` to an iterable sequence of int

    Parameters
    ----------
    x : value, or sequence of values, convertible to int
    name : str, optional
        Name of the argument being converted, only used in the error message

    Returns
    -------
    y : ``list[int]``
    """
    if isinstance(x, Number):
        x = (x,)

    try:
        x = [operator.index(a) for a in x]
    except TypeError as e:
        name = name or "value"
        raise ValueError(f"{name} must be a scalar or iterable of integers") from e

    return x

