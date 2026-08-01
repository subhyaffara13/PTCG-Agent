
def boxplot(
    x: ArrayLike | Sequence[ArrayLike],
    notch: bool | None = None,
    sym: str | None = None,
    vert: bool | None = None,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    whis: float | tuple[float, float] | None = None,
    positions: ArrayLike | None = None,
    widths: float | ArrayLike | None = None,
    patch_artist: bool | None = None,
    bootstrap: int | None = None,
    usermedians: ArrayLike | None = None,
    conf_intervals: ArrayLike | None = None,
    meanline: bool | None = None,
    showmeans: bool | None = None,
    showcaps: bool | None = None,
    showbox: bool | None = None,
    showfliers: bool | None = None,
    boxprops: dict[str, Any] | None = None,
    tick_labels: Sequence[str] | None = None,
    flierprops: dict[str, Any] | None = None,
    medianprops: dict[str, Any] | None = None,
    meanprops: dict[str, Any] | None = None,
    capprops: dict[str, Any] | None = None,
    whiskerprops: dict[str, Any] | None = None,
    manage_ticks: bool = True,
    autorange: bool = False,
    zorder: float | None = None,
    capwidths: float | ArrayLike | None = None,
    label: Sequence[str] | None = None,
    *,
    data: DataParamType = None,
) -> dict[str, Any]:
    return gca().boxplot(
        x,
        notch=notch,
        sym=sym,
        vert=vert,
        orientation=orientation,
        whis=whis,
        positions=positions,
        widths=widths,
        patch_artist=patch_artist,
        bootstrap=bootstrap,
        usermedians=usermedians,
        conf_intervals=conf_intervals,
        meanline=meanline,
        showmeans=showmeans,
        showcaps=showcaps,
        showbox=showbox,
        showfliers=showfliers,
        boxprops=boxprops,
        tick_labels=tick_labels,
        flierprops=flierprops,
        medianprops=medianprops,
        meanprops=meanprops,
        capprops=capprops,
        whiskerprops=whiskerprops,
        manage_ticks=manage_ticks,
        autorange=autorange,
        zorder=zorder,
        capwidths=capwidths,
        label=label,
        **({"data": data} if data is not None else {}),
    )


def boxplot(
    data=None, *, x=None, y=None, hue=None, order=None, hue_order=None,
    orient=None, color=None, palette=None, saturation=.75, fill=True,
    dodge="auto", width=.8, gap=0, whis=1.5, linecolor="auto", linewidth=None,
    fliersize=None, hue_norm=None, native_scale=False, log_scale=None, formatter=None,
    legend="auto", ax=None, **kwargs
):

    p = _CategoricalPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue),
        order=order,
        orient=orient,
        color=color,
        legend=legend,
    )

    if ax is None:
        ax = plt.gca()

    if p.plot_data.empty:
        return ax

    if dodge == "auto":
        # Needs to be before scale_categorical changes the coordinate series dtype
        dodge = p._dodge_needed()

    if p.var_types.get(p.orient) == "categorical" or not native_scale:
        p.scale_categorical(p.orient, order=order, formatter=formatter)

    p._attach(ax, log_scale=log_scale)

    # Deprecations to remove in v0.14.0.
    hue_order = p._palette_without_hue_backcompat(palette, hue_order)
    palette, hue_order = p._hue_backcompat(color, palette, hue_order)

    saturation = saturation if fill else 1
    p.map_hue(palette=palette, order=hue_order, norm=hue_norm, saturation=saturation)
    color = _default_color(
        ax.fill_between, hue, color,
        {k: v for k, v in kwargs.items() if k in ["c", "color", "fc", "facecolor"]},
        saturation=saturation,
    )
    linecolor = p._complement_color(linecolor, color, p._hue_map)

    p.plot_boxes(
        width=width,
        dodge=dodge,
        gap=gap,
        fill=fill,
        whis=whis,
        color=color,
        linecolor=linecolor,
        linewidth=linewidth,
        fliersize=fliersize,
        plot_kws=kwargs,
    )

    p._add_axis_labels(ax)
    p._adjust_cat_axis(ax, axis=p.orient)

    return ax


def boxplot(
    data: DataFrame,
    column: str | list[str] | None = None,
    by: str | list[str] | None = None,
    ax: Axes | None = None,
    fontsize: float | str | None = None,
    rot: int = 0,
    grid: bool = True,
    figsize: tuple[float, float] | None = None,
    layout: tuple[int, int] | None = None,
    return_type: str | None = None,
    **kwargs,
):
    """
    Make a box plot from DataFrame columns.

    Make a box-and-whisker plot from DataFrame columns, optionally grouped
    by some other columns. A box plot is a method for graphically depicting
    groups of numerical data through their quartiles.
    The box extends from the Q1 to Q3 quartile values of the data,
    with a line at the median (Q2). The whiskers extend from the edges
    of box to show the range of the data. By default, they extend no more than
    `1.5 * IQR (IQR = Q3 - Q1)` from the edges of the box, ending at the farthest
    data point within that interval. Outliers are plotted as separate dots.

    For further details see
    Wikipedia's entry for `boxplot <https://en.wikipedia.org/wiki/Box_plot>`_.

    Parameters
    ----------
    data : DataFrame
        The data to visualize.
    column : str or list of str, optional
        Column name or list of names, or vector.
        Can be any valid input to :meth:`pandas.DataFrame.groupby`.
    by : str or array-like, optional
        Column in the DataFrame to :meth:`pandas.DataFrame.groupby`.
        One box-plot will be done per value of columns in `by`.
    ax : object of class matplotlib.axes.Axes, optional
        The matplotlib axes to be used by boxplot.
    fontsize : float or str
        Tick label font size in points or as a string (e.g., `large`).
    rot : float, default 0
        The rotation angle of labels (in degrees)
        with respect to the screen coordinate system.
    grid : bool, default True
        Setting this to True will show the grid.
    figsize : A tuple (width, height) in inches
        The size of the figure to create in matplotlib.
    layout : tuple (rows, columns), optional
        For example, (3, 5) will display the subplots
        using 3 rows and 5 columns, starting from the top-left.
    return_type : {'axes', 'dict', 'both'} or None, default 'axes'
        The kind of object to return. The default is ``axes``.

        * 'axes' returns the matplotlib axes the boxplot is drawn on.
        * 'dict' returns a dictionary whose values are the matplotlib
          lines of the boxplot.
        * 'both' returns a namedtuple with the axes and dict.
        * when grouping with ``by``, a Series mapping columns to
          ``return_type`` is returned.

        If ``return_type`` is `None`, a NumPy array
        of axes with the same shape as ``layout`` is returned.

    **kwargs
        All other plotting keyword arguments to be passed to
        :func:`matplotlib.pyplot.boxplot`.

    Returns
    -------
    result
        See Notes.

    See Also
    --------
    Series.plot.hist: Make a histogram.
    matplotlib.pyplot.boxplot : Matplotlib equivalent plot.

    Notes
    -----
    The return type depends on the `return_type` parameter:

    * 'axes' : object of class matplotlib.axes.Axes
    * 'dict' : dict of matplotlib.lines.Line2D objects
    * 'both' : a namedtuple with structure (ax, lines)

    For data grouped with ``by``, return a Series of the above or a numpy
    array:

    * :class:`~pandas.Series`
    * :class:`~numpy.array` (for ``return_type = None``)

    Use ``return_type='dict'`` when you want to tweak the appearance
    of the lines after plotting. In this case a dict containing the Lines
    making up the boxes, caps, fliers, medians, and whiskers is returned.

    Examples
    --------

    Boxplots can be created for every column in the dataframe
    by ``df.boxplot()`` or indicating the columns to be used:

    .. plot::
        :context: close-figs

        >>> np.random.seed(1234)
        >>> df = pd.DataFrame(
        ...     np.random.randn(10, 4), columns=["Col1", "Col2", "Col3", "Col4"]
        ... )
        >>> boxplot = df.boxplot(column=["Col1", "Col2", "Col3"])  # doctest: +SKIP

    Boxplots of variables distributions grouped by the values of a third
    variable can be created using the option ``by``. For instance:

    .. plot::
        :context: close-figs

        >>> df = pd.DataFrame(np.random.randn(10, 2), columns=["Col1", "Col2"])
        >>> df["X"] = pd.Series(["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"])
        >>> boxplot = df.boxplot(by="X")

    A list of strings (i.e. ``['X', 'Y']``) can be passed to boxplot
    in order to group the data by combination of the variables in the x-axis:

    .. plot::
        :context: close-figs

        >>> df = pd.DataFrame(np.random.randn(10, 3), columns=["Col1", "Col2", "Col3"])
        >>> df["X"] = pd.Series(["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"])
        >>> df["Y"] = pd.Series(["A", "B", "A", "B", "A", "B", "A", "B", "A", "B"])
        >>> boxplot = df.boxplot(column=["Col1", "Col2"], by=["X", "Y"])

    The layout of boxplot can be adjusted giving a tuple to ``layout``:

    .. plot::
        :context: close-figs

        >>> boxplot = df.boxplot(column=["Col1", "Col2"], by="X", layout=(2, 1))

    Additional formatting can be done to the boxplot, like suppressing the grid
    (``grid=False``), rotating the labels in the x-axis (i.e. ``rot=45``)
    or changing the fontsize (i.e. ``fontsize=15``):

    .. plot::
        :context: close-figs

        >>> boxplot = df.boxplot(grid=False, rot=45, fontsize=15)  # doctest: +SKIP

    The parameter ``return_type`` can be used to select the type of element
    returned by `boxplot`.  When ``return_type='axes'`` is selected,
    the matplotlib axes on which the boxplot is drawn are returned:

        >>> boxplot = df.boxplot(column=["Col1", "Col2"], return_type="axes")
        >>> type(boxplot)
        <class 'matplotlib.axes._axes.Axes'>

    When grouping with ``by``, a Series mapping columns to ``return_type``
    is returned:

        >>> boxplot = df.boxplot(column=["Col1", "Col2"], by="X", return_type="axes")
        >>> type(boxplot)
        <class 'pandas.Series'>

    If ``return_type`` is `None`, a NumPy array of axes with the same shape
    as ``layout`` is returned:

        >>> boxplot = df.boxplot(column=["Col1", "Col2"], by="X", return_type=None)
        >>> type(boxplot)
        <class 'numpy.ndarray'>
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.boxplot(
        data,
        column=column,
        by=by,
        ax=ax,
        fontsize=fontsize,
        rot=rot,
        grid=grid,
        figsize=figsize,
        layout=layout,
        return_type=return_type,
        **kwargs,
    )


def boxplot(
    data,
    column=None,
    by=None,
    ax=None,
    fontsize: int | None = None,
    rot: int = 0,
    grid: bool = True,
    figsize: tuple[float, float] | None = None,
    layout=None,
    return_type=None,
    **kwds,
):
    import matplotlib.pyplot as plt

    # validate return_type:
    if return_type not in BoxPlot._valid_return_types:
        raise ValueError("return_type must be {'axes', 'dict', 'both'}")

    if isinstance(data, ABCSeries):
        data = data.to_frame("x")
        column = "x"

    def _get_colors():
        #  num_colors=3 is required as method maybe_color_bp takes the colors
        #  in positions 0 and 2.
        #  if colors not provided, use same defaults as DataFrame.plot.box
        result_list = get_standard_colors(num_colors=3)
        result = np.take(result_list, [0, 0, 2])
        result = np.append(result, "k")

        colors = kwds.pop("color", None)
        if colors:
            if is_dict_like(colors):
                # replace colors in result array with user-specified colors
                # taken from the colors dict parameter
                # "boxes" value placed in position 0, "whiskers" in 1, etc.
                valid_keys = ["boxes", "whiskers", "medians", "caps"]
                key_to_index = dict(zip(valid_keys, range(4), strict=True))
                for key, value in colors.items():
                    if key in valid_keys:
                        result[key_to_index[key]] = value
                    else:
                        raise ValueError(
                            f"color dict contains invalid key '{key}'. "
                            f"The key must be either {valid_keys}"
                        )
            else:
                result.fill(colors)

        return result

    def plot_group(keys, values, ax: Axes, **kwds):
        # GH 45465: xlabel/ylabel need to be popped out before plotting happens
        xlabel, ylabel = kwds.pop("xlabel", None), kwds.pop("ylabel", None)
        if xlabel:
            ax.set_xlabel(pprint_thing(xlabel))
        if ylabel:
            ax.set_ylabel(pprint_thing(ylabel))

        keys = [pprint_thing(x) for x in keys]
        values = [remove_na_arraylike(v) for v in values]
        bp = ax.boxplot(values, **kwds)
        if fontsize is not None:
            ax.tick_params(axis="both", labelsize=fontsize)

        # GH 45465: x/y are flipped when "vert" changes
        _set_ticklabels(
            ax=ax, labels=keys, is_vertical=kwds.get("vert", True), rotation=rot
        )
        maybe_color_bp(bp, color_tup=colors, **kwds)

        # Return axes in multiplot case, maybe revisit later # 985
        if return_type == "dict":
            return bp
        elif return_type == "both":
            return BoxPlot.BP(ax=ax, lines=bp)
        else:
            return ax

    colors = _get_colors()
    if column is None:
        columns = None
    elif isinstance(column, (list, tuple)):
        columns = column
    else:
        columns = [column]

    if by is not None:
        # Prefer array return type for 2-D plots to match the subplot layout
        # https://github.com/pandas-dev/pandas/pull/12216#issuecomment-241175580
        result = _grouped_plot_by_column(
            plot_group,
            data,
            columns=columns,
            by=by,
            grid=grid,
            figsize=figsize,
            ax=ax,
            layout=layout,
            return_type=return_type,
            **kwds,
        )
    else:
        if return_type is None:
            return_type = "axes"
        if layout is not None:
            raise ValueError("The 'layout' keyword is not supported when 'by' is None")

        if ax is None:
            rc = {"figure.figsize": figsize} if figsize is not None else {}
            with mpl.rc_context(rc):
                ax = plt.gca()
        data = data._get_numeric_data()
        naxes = len(data.columns)
        if naxes == 0:
            raise ValueError(
                "boxplot method requires numerical columns, nothing to plot."
            )
        if columns is None:
            columns = data.columns
        else:
            data = data[columns]

        result = plot_group(columns, data.values.T, ax, **kwds)
        ax.grid(grid)

    return result

