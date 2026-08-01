
def parallel_coordinates(
    frame: DataFrame,
    class_column: str,
    cols: list[str] | None = None,
    ax: Axes | None = None,
    color: list[str] | tuple[str, ...] | None = None,
    use_columns: bool = False,
    xticks: list | tuple | None = None,
    colormap: Colormap | str | None = None,
    axvlines: bool = True,
    axvlines_kwds: Mapping[str, Any] | None = None,
    sort_labels: bool = False,
    **kwargs,
) -> Axes:
    """
    Parallel coordinates plotting.

    Parameters
    ----------
    frame : DataFrame
        The DataFrame to be plotted.
    class_column : str
        Column name containing class names.
    cols : list, optional
        A list of column names to use.
    ax : matplotlib.axis, optional
        Matplotlib axis object.
    color : list or tuple, optional
        Colors to use for the different classes.
    use_columns : bool, optional
        If true, columns will be used as xticks.
    xticks : list or tuple, optional
        A list of values to use for xticks.
    colormap : str or matplotlib colormap, default None
        Colormap to use for line colors.
    axvlines : bool, optional
        If true, vertical lines will be added at each xtick.
    axvlines_kwds : keywords, optional
        Options to be passed to axvline method for vertical lines.
    sort_labels : bool, default False
        Sort class_column labels, useful when assigning colors.
    **kwargs
        Options to pass to matplotlib plotting method.

    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib axes containing the parallel coordinates plot.

    See Also
    --------
    plotting.andrews_curves : Generate a matplotlib plot for visualizing clusters
        of multivariate data.
    plotting.radviz : Plot a multidimensional dataset in 2D.

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> df = pd.read_csv(
        ...     "https://raw.githubusercontent.com/pandas-dev/"
        ...     "pandas/main/pandas/tests/io/data/csv/iris.csv"
        ... )  # doctest: +SKIP
        >>> pd.plotting.parallel_coordinates(
        ...     df, "Name", color=("#556270", "#4ECDC4", "#C7F464")
        ... )  # doctest: +SKIP
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.parallel_coordinates(
        frame=frame,
        class_column=class_column,
        cols=cols,
        ax=ax,
        color=color,
        use_columns=use_columns,
        xticks=xticks,
        colormap=colormap,
        axvlines=axvlines,
        axvlines_kwds=axvlines_kwds,
        sort_labels=sort_labels,
        **kwargs,
    )


def parallel_coordinates(
    frame: DataFrame,
    class_column,
    cols=None,
    ax: Axes | None = None,
    color=None,
    use_columns: bool = False,
    xticks=None,
    colormap=None,
    axvlines: bool = True,
    axvlines_kwds=None,
    sort_labels: bool = False,
    **kwds,
) -> Axes:
    import matplotlib.pyplot as plt

    if axvlines_kwds is None:
        axvlines_kwds = {"linewidth": 1, "color": "black"}

    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]

    if cols is None:
        df = frame.drop(class_column, axis=1)
    else:
        df = frame[cols]

    used_legends: set[str] = set()

    ncols = len(df.columns)

    # determine values to use for xticks
    x: list[int] | Index
    if use_columns is True:
        if not np.all(np.isreal(list(df.columns))):
            raise ValueError("Columns must be numeric to be used as xticks")
        x = df.columns
    elif xticks is not None:
        if not np.all(np.isreal(xticks)):
            raise ValueError("xticks specified must be numeric")
        if len(xticks) != ncols:
            raise ValueError("Length of xticks must match number of columns")
        x = xticks
    else:
        x = list(range(ncols))

    if ax is None:
        ax = plt.gca()

    color_values = get_standard_colors(
        num_colors=len(classes), colormap=colormap, color_type="random", color=color
    )

    if sort_labels:
        classes = sorted(classes)
        color_values = sorted(color_values)
    colors = dict(zip(classes, color_values, strict=True))

    for i in range(n):
        y = df.iloc[i].values
        kls = class_col.iat[i]
        label = pprint_thing(kls)
        if label not in used_legends:
            used_legends.add(label)
            ax.plot(x, y, color=colors[kls], label=label, **kwds)
        else:
            ax.plot(x, y, color=colors[kls], **kwds)

    if axvlines:
        for i in x:
            ax.axvline(i, **axvlines_kwds)

    ax.set_xticks(x)
    ax.set_xticklabels(df.columns)
    ax.set_xlim(x[0], x[-1])
    ax.legend(loc="upper right")
    ax.grid()
    return ax

