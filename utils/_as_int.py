
def _as_int(value: str | None) -> int | None:
    if value is None:
        return None
    return int(value)


def _as_int(x, desc):
    """
    Like `operator.index`, but emits a custom exception when passed an
    incorrect type

    Parameters
    ----------
    x : int-like
        Value to interpret as an integer
    desc : str
        description to include in any error message

    Raises
    ------
    TypeError : if x is a float or non-numeric
    """
    try:
        return operator.index(x)
    except TypeError as e:
        raise TypeError(f"{desc} must be an integer, received {x}") from e

