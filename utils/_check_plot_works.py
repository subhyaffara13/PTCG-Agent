
def _check_plot_works(f, default_axes=False, **kwargs):
    """
    Create plot and ensure that plot return object is valid.

    Parameters
    ----------
    f : func
        Plotting function.
    default_axes : bool, optional
        If False (default):
            - If `ax` not in `kwargs`, then create subplot(211) and plot there
            - Create new subplot(212) and plot there as well
            - Mind special corner case for bootstrap_plot (see `_gen_two_subplots`)
        If True:
            - Simply run plotting function with kwargs provided
            - All required axes instances will be created automatically
            - It is recommended to use it when the plotting function
            creates multiple axes itself. It helps avoid warnings like
            'UserWarning: To output multiple subplots,
            the figure containing the passed axes is being cleared'
    **kwargs
        Keyword arguments passed to the plotting function.

    Returns
    -------
    Plot object returned by the last plotting.
    """
    import matplotlib.pyplot as plt

    if default_axes:
        gen_plots = _gen_default_plot
    else:
        gen_plots = _gen_two_subplots

    ret = None
    fig = kwargs.get("figure", plt.gcf())
    fig.clf()

    for ret in gen_plots(f, fig, **kwargs):
        assert_is_valid_plot_return_object(ret)

    return ret


def _check_plot_works(f, freq=None, series=None, *args, **kwargs):
    fig = plt.gcf()

    fig.clf()
    ax = fig.add_subplot(211)
    orig_ax = kwargs.pop("ax", plt.gca())
    orig_axfreq = getattr(orig_ax, "freq", None)

    ret = f(*args, **kwargs)
    assert ret is not None  # do something more intelligent

    ax = kwargs.pop("ax", plt.gca())
    if series is not None:
        dfreq = series.index.freq
        if isinstance(dfreq, BaseOffset):
            dfreq = dfreq.rule_code
        if orig_axfreq is None:
            assert ax.freq == dfreq

    if freq is not None and orig_axfreq is None:
        assert to_offset(ax.freq, is_period=True) == freq

    ax = fig.add_subplot(212)
    kwargs["ax"] = ax
    ret = f(*args, **kwargs)
    assert ret is not None  # TODO: do something more intelligent

