
def boxplot_frame_groupby(
    grouped: DataFrameGroupBy,
    subplots: bool = True,
    column=None,
    fontsize: int | None = None,
    rot: int = 0,
    grid: bool = True,
    ax=None,
    figsize: tuple[float, float] | None = None,
    layout=None,
    sharex: bool = False,
    sharey: bool = True,
    backend=None,
    **kwargs,
):
    """
    Make box plots from DataFrameGroupBy data.

    Parameters
    ----------
    grouped : DataFrameGroupBy
        The grouped DataFrame object over which to create the box plots.
    subplots : bool
        * ``False`` - no subplots will be used
        * ``True`` - create a subplot for each group.
    column : column name or list of names, or vector
        Can be any valid input to groupby.
    fontsize : float or str
        Font size for the labels.
    rot : float
        Rotation angle of labels (in degrees) on the x-axis.
    grid : bool
        Whether to show grid lines on the plot.
    ax : Matplotlib axis object, default None
        The axes on which to draw the plots. If None, uses the current axes.
    figsize : tuple of (float, float)
        The figure size in inches (width, height).
    layout : tuple (optional)
        The layout of the plot: (rows, columns).
    sharex : bool, default False
        Whether x-axes will be shared among subplots.
    sharey : bool, default True
        Whether y-axes will be shared among subplots.
    backend : str, default None
        Backend to use instead of the backend specified in the option
        ``plotting.backend``. For instance, 'matplotlib'. Alternatively, to
        specify the ``plotting.backend`` for the whole session, set
        ``pd.options.plotting.backend``.
    **kwargs
        All other plotting keyword arguments to be passed to
        matplotlib's boxplot function.

    Returns
    -------
    dict or DataFrame.boxplot return value
        If ``subplots=True``, returns a dictionary of group keys to the boxplot
        return values. If ``subplots=False``, returns the boxplot return value
        of a single DataFrame.

    See Also
    --------
    DataFrame.boxplot : Create a box plot from a DataFrame.
    Series.plot : Plot a Series.

    Examples
    --------
    You can create boxplots for grouped data and show them as separate subplots:

    .. plot::
        :context: close-figs

        >>> import itertools
        >>> tuples = [t for t in itertools.product(range(1000), range(4))]
        >>> index = pd.MultiIndex.from_tuples(tuples, names=["lvl0", "lvl1"])
        >>> data = np.random.randn(len(index), 4)
        >>> df = pd.DataFrame(data, columns=list("ABCD"), index=index)
        >>> grouped = df.groupby(level="lvl1")
        >>> grouped.boxplot(rot=45, fontsize=12, figsize=(8, 10))  # doctest: +SKIP

    The ``subplots=False`` option shows the boxplots in a single figure.

    .. plot::
        :context: close-figs

        >>> grouped.boxplot(subplots=False, rot=45, fontsize=12)  # doctest: +SKIP
    """
    plot_backend = _get_plot_backend(backend)
    return plot_backend.boxplot_frame_groupby(
        grouped,
        subplots=subplots,
        column=column,
        fontsize=fontsize,
        rot=rot,
        grid=grid,
        ax=ax,
        figsize=figsize,
        layout=layout,
        sharex=sharex,
        sharey=sharey,
        **kwargs,
    )


def boxplot_frame_groupby(
    grouped,
    subplots: bool = True,
    column=None,
    fontsize: int | None = None,
    rot: int = 0,
    grid: bool = True,
    ax=None,
    figsize: tuple[float, float] | None = None,
    layout=None,
    sharex: bool = False,
    sharey: bool = True,
    **kwds,
):
    if subplots is True:
        naxes = len(grouped)
        fig, axes = create_subplots(
            naxes=naxes,
            squeeze=False,
            ax=ax,
            sharex=sharex,
            sharey=sharey,
            figsize=figsize,
            layout=layout,
        )
        data = {}
        for (key, group), ax in zip(grouped, flatten_axes(axes), strict=False):
            d = group.boxplot(
                ax=ax, column=column, fontsize=fontsize, rot=rot, grid=grid, **kwds
            )
            ax.set_title(pprint_thing(key))
            data[key] = d
        ret = pd.Series(data)
        maybe_adjust_figure(fig, bottom=0.15, top=0.9, left=0.1, right=0.9, wspace=0.2)
    else:
        keys, frames = zip(*grouped, strict=True)
        df = pd.concat(frames, keys=keys, axis=1)

        # GH 16748, DataFrameGroupby fails when subplots=False and `column` argument
        # is assigned, and in this case, since `df` here becomes MI after groupby,
        # so we need to couple the keys (grouped values) and column (original df
        # column) together to search for subset to plot
        if column is not None:
            column = com.convert_to_list_like(column)
            multi_key = pd.MultiIndex.from_product([keys, column])
            column = list(multi_key.values)
        ret = df.boxplot(
            column=column,
            fontsize=fontsize,
            rot=rot,
            grid=grid,
            ax=ax,
            figsize=figsize,
            layout=layout,
            **kwds,
        )
    return ret

