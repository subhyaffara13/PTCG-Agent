
def validate_kwargs(valid_processor_keys: list[str], captured_kwargs: list[str]):
    unused_keys = set(captured_kwargs).difference(set(valid_processor_keys))
    if unused_keys:
        unused_key_str = ", ".join(unused_keys)
        # TODO raise a warning here instead of simply logging?
        logger.warning(f"Unused or unrecognized kwargs: {unused_key_str}.")


def validate_kwargs(fname, kwargs, compat_args) -> None:
    """
    Checks whether parameters passed to the **kwargs argument in a
    function `fname` are valid parameters as specified in `*compat_args`
    and whether or not they are set to their default values.

    Parameters
    ----------
    fname : str
        The name of the function being passed the `**kwargs` parameter
    kwargs : dict
        The `**kwargs` parameter passed into `fname`
    compat_args: dict
        A dictionary of keys that `kwargs` is allowed to have and their
        associated default values

    Raises
    ------
    TypeError if `kwargs` contains keys not in `compat_args`
    ValueError if `kwargs` contains keys in `compat_args` that do not
    map to the default values specified in `compat_args`
    """
    kwds = kwargs.copy()
    _check_for_invalid_keys(fname, kwargs, compat_args)
    _check_for_default_values(fname, kwds, compat_args)

