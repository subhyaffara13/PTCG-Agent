
def validate_na_arg(value, name: str):
    """
    Validate na arguments.

    Parameters
    ----------
    value : object
        Value to validate.
    name : str
        Name of the argument, used to raise an informative error message.

    Raises
    ______
    ValueError
        When ``value`` is determined to be invalid.
    """
    if (
        value is lib.no_default
        or isinstance(value, bool)
        or value is None
        or value is NA
        or (lib.is_float(value) and np.isnan(value))
    ):
        return
    raise ValueError(f"{name} must be None, pd.NA, np.nan, True, or False; got {value}")

