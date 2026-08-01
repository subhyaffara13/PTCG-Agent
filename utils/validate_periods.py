
def validate_periods(periods: None) -> None: ...


def validate_periods(periods: int) -> int: ...


def validate_periods(periods: int | None) -> int | None:
    """
    If a `periods` argument is passed to the Datetime/Timedelta Array/Index
    constructor, cast it to an integer.

    Parameters
    ----------
    periods : None, int

    Returns
    -------
    periods : None or int

    Raises
    ------
    TypeError
        if periods is not None or int
    """
    if periods is not None and not lib.is_integer(periods):
        raise TypeError(f"periods must be an integer, got {periods}")
    # error: Incompatible return value type (got "int | integer[Any] | None",
    # expected "int | None")
    return periods  # type: ignore[return-value]

