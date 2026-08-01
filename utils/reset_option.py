
def reset_option(pat: str) -> None:
    """
    Reset one or more options to their default value.

    This method resets the specified pandas option(s) back to their default
    values. It allows partial string matching for convenience, but users should
    exercise caution to avoid unintended resets due to changes in option names
    in future versions.

    Parameters
    ----------
    pat : str/regex
        If specified only options matching ``pat*`` will be reset.
        Pass ``"all"`` as argument to reset all options.

        .. warning::

            Partial matches are supported for convenience, but unless you
            use the full option name (e.g. x.y.z.option_name), your code may break
            in future versions if new options with similar names are introduced.

    Returns
    -------
    None
        No return value.

    See Also
    --------
    get_option : Retrieve the value of the specified option.
    set_option : Set the value of the specified option or options.
    describe_option : Print the description for one or more registered options.

    Notes
    -----
    For all available options, please view the
    :ref:`User Guide <options.available>`.

    Examples
    --------
    >>> pd.reset_option("display.max_columns")  # doctest: +SKIP
    """
    keys = _select_options(pat)

    if len(keys) == 0:
        raise OptionError(f"No such keys(s) for {pat=}")

    if len(keys) > 1 and len(pat) < 4 and pat != "all":
        raise ValueError(
            "You must specify at least 4 characters when "
            "resetting multiple keys, use the special keyword "
            '"all" to reset all the options to their default value'
        )

    for k in keys:
        set_option(k, _registered_options[k].defval)

