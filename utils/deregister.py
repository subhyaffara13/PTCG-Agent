
def deregister() -> None:
    """
    Remove pandas formatters and converters.

    Removes the custom converters added by :func:`register`. This
    attempts to set the state of the registry back to the state before
    pandas registered its own units. Converters for pandas' own types like
    Timestamp and Period are removed completely. Converters for types
    pandas overwrites, like ``datetime.datetime``, are restored to their
    original value.

    See Also
    --------
    register_matplotlib_converters : Register pandas formatters and converters
        with matplotlib.

    Examples
    --------
    .. plot::
       :context: close-figs

        The following line is done automatically by pandas so
        the plot can be rendered:

        >>> pd.plotting.register_matplotlib_converters()

        >>> df = pd.DataFrame(
        ...     {"ts": pd.period_range("2020", periods=2, freq="M"), "y": [1, 2]}
        ... )
        >>> plot = df.plot.line(x="ts", y="y")

    Unsetting the register manually an error will be raised:

    >>> pd.set_option(
    ...     "plotting.matplotlib.register_converters", False
    ... )  # doctest: +SKIP
    >>> df.plot.line(x="ts", y="y")  # doctest: +SKIP
    Traceback (most recent call last):
    TypeError: float() argument must be a string or a real number, not 'Period'
    """
    plot_backend = _get_plot_backend("matplotlib")
    plot_backend.deregister()


def deregister() -> None:
    # Renamed in pandas.plotting.__init__
    for type_, cls in get_pairs():
        # We use type to catch our classes directly, no inheritance
        if type(munits.registry.get(type_)) is cls:
            munits.registry.pop(type_)

    # restore the old keys
    for unit, formatter in _mpl_units.items():
        if type(formatter) not in {DatetimeConverter, PeriodConverter, TimeConverter}:
            # make it idempotent by excluding ours.
            munits.registry[unit] = formatter

