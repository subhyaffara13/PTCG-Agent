
def is_nonnegative_int(value: object) -> None:
    """
    Verify that value is None or a positive int.

    Parameters
    ----------
    value : None or int
            The `value` to be checked.

    Raises
    ------
    ValueError
        When the value is not None or is a negative integer
    """
    if value is None:
        return

    elif isinstance(value, int):
        if value >= 0:
            return

    msg = "Value must be a nonnegative integer or None"
    raise ValueError(msg)

