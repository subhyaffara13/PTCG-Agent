
def validate_fillna_kwargs(value, method, validate_scalar_dict_value: bool = True):
    """
    Validate the keyword arguments to 'fillna'.

    This checks that exactly one of 'value' and 'method' is specified.
    If 'method' is specified, this validates that it's a valid method.

    Parameters
    ----------
    value, method : object
        The 'value' and 'method' keyword arguments for 'fillna'.
    validate_scalar_dict_value : bool, default True
        Whether to validate that 'value' is a scalar or dict. Specifically,
        validate that it is not a list or tuple.

    Returns
    -------
    value, method : object
    """
    from pandas.core.missing import clean_fill_method

    if value is None and method is None:
        raise ValueError("Must specify a fill 'value' or 'method'.")
    if value is None and method is not None:
        method = clean_fill_method(method)

    elif value is not None and method is None:
        if validate_scalar_dict_value and isinstance(value, (list, tuple)):
            raise TypeError(
                '"value" parameter must be a scalar or dict, but '
                f'you passed a "{type(value).__name__}"'
            )

    elif value is not None and method is not None:
        raise ValueError("Cannot specify both 'value' and 'method'.")

    return value, method

