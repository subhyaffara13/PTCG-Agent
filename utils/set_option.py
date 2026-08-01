
def set_option(*args) -> None:
    """
    Set the value of the specified option or options.

    This method allows fine-grained control over the behavior and display settings
    of pandas. Options affect various functionalities such as output formatting,
    display limits, and operational behavior. Settings can be modified at runtime
    without requiring changes to global configurations or environment variables.

    Parameters
    ----------
    *args : str | object | dict
        Arguments provided in pairs, which will be interpreted as (pattern, value),
        or as a single dictionary containing multiple option-value pairs.
        pattern: str
        Regexp which should match a single option
        value: object
        New value of option

        .. warning::

            Partial pattern matches are supported for convenience, but unless you
            use the full option name (e.g. x.y.z.option_name), your code may break in
            future versions if new options with similar names are introduced.

    Returns
    -------
    None
        No return value.

    Raises
    ------
    ValueError if odd numbers of non-keyword arguments are provided
    TypeError if keyword arguments are provided
    OptionError if no such option exists

    See Also
    --------
    get_option : Retrieve the value of the specified option.
    reset_option : Reset one or more options to their default value.
    describe_option : Print the description for one or more registered options.
    option_context : Context manager to temporarily set options in a ``with``
        statement.

    Notes
    -----
    For all available options, please view the :ref:`User Guide <options.available>`
    or use ``pandas.describe_option()``.

    Examples
    --------
    Option-Value Pair Input:

    >>> pd.set_option("display.max_columns", 4)
    >>> df = pd.DataFrame([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    >>> df
    0  1  ...  3   4
    0  1  2  ...  4   5
    1  6  7  ...  9  10
    [2 rows x 5 columns]
    >>> pd.reset_option("display.max_columns")

    Dictionary Input:

    >>> pd.set_option({"display.max_columns": 4, "display.precision": 1})
    >>> df = pd.DataFrame([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    >>> df
    0  1  ...  3   4
    0  1  2  ...  4   5
    1  6  7  ...  9  10
    [2 rows x 5 columns]
    >>> pd.reset_option("display.max_columns")
    >>> pd.reset_option("display.precision")
    """
    # Handle dictionary input
    if len(args) == 1 and isinstance(args[0], dict):
        args = tuple(kv for item in args[0].items() for kv in item)

    nargs = len(args)
    if not nargs or nargs % 2 != 0:
        raise ValueError("Must provide an even number of non-keyword arguments")

    for k, v in zip(args[::2], args[1::2], strict=True):
        key = _get_single_key(k)

        opt = _get_registered_option(key)
        if opt and opt.validator:
            opt.validator(v)

        # walk the nested dict
        root, k_root = _get_root(key)
        root[k_root] = v

        if opt.cb:
            opt.cb(key)

