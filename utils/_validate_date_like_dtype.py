
def _validate_date_like_dtype(dtype) -> None:
    """
    Check whether the dtype is a date-like dtype. Raises an error if invalid.

    Parameters
    ----------
    dtype : dtype, type
        The dtype to check.

    Raises
    ------
    TypeError : The dtype could not be casted to a date-like dtype.
    ValueError : The dtype is an illegal date-like dtype (e.g. the
                 frequency provided is too specific)
    """
    try:
        typ = np.datetime_data(dtype)[0]
    except ValueError as e:
        raise TypeError(e) from e
    if typ not in ["generic", "ns"]:
        raise ValueError(
            f"{dtype.name!r} is too specific of a frequency, "
            f"try passing {dtype.type.__name__!r}"
        )

