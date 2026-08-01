
def validate_args(fname, args, max_fname_arg_count, compat_args) -> None:
    """
    Checks whether the length of the `*args` argument passed into a function
    has at most `len(compat_args)` arguments and whether or not all of these
    elements in `args` are set to their default values.

    Parameters
    ----------
    fname : str
        The name of the function being passed the `*args` parameter
    args : tuple
        The `*args` parameter passed into a function
    max_fname_arg_count : int
        The maximum number of arguments that the function `fname`
        can accept, excluding those in `args`. Used for displaying
        appropriate error messages. Must be non-negative.
    compat_args : dict
        A dictionary of keys and their associated default values.
        In order to accommodate buggy behaviour in some versions of `numpy`,
        where a signature displayed keyword arguments but then passed those
        arguments **positionally** internally when calling downstream
        implementations, a dict ensures that the original
        order of the keyword arguments is enforced.

    Raises
    ------
    TypeError
        If `args` contains more values than there are `compat_args`
    ValueError
        If `args` contains values that do not correspond to those
        of the default values specified in `compat_args`
    """
    _check_arg_length(fname, args, max_fname_arg_count, compat_args)

    # We do this so that we can provide a more informative
    # error message about the parameters that we are not
    # supporting in the pandas implementation of 'fname'
    kwargs = dict(zip(compat_args, args, strict=False))
    _check_for_default_values(fname, kwargs, compat_args)

