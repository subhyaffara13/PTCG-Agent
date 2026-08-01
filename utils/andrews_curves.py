
def andrews_curves(
    frame: DataFrame,
    class_column: str,
    ax: Axes | None = None,
    samples: int = 200,
    color: list[str] | tuple[str, ...] | None = None,
    colormap: Colormap | str | None = None,
    **kwargs,
) -> Axes:
    """
    Generate a matplotlib plot for visualizing clusters of multivariate data.

    Andrews curves have the functional form:

    .. math::
        f(t) = \\frac{x_1}{\\sqrt{2}} + x_2 \\sin(t) + x_3 \\cos(t) +
        x_4 \\sin(2t) + x_5 \\cos(2t) + \\cdots

    Where :math:`x` coefficients correspond to the values of each dimension
    and :math:`t` is linearly spaced between :math:`-\\pi` and :math:`+\\pi`.
    Each row of frame then corresponds to a single curve.

    Parameters
    ----------
    frame : DataFrame
        Data to be plotted, preferably normalized to (0.0, 1.0).
    class_column : label
        Name of the column containing class names.
    ax : axes object, default None
        Axes to use.
    samples : int
        Number of points to plot in each curve.
    color : str, list[str] or tuple[str], optional
        Colors to use for the different classes. Colors can be strings
        or 3-element floating point RGB values.
    colormap : str or matplotlib colormap object, default None
        Colormap to select colors from. If a string, load colormap with that
        name from matplotlib.
    **kwargs
        Options to pass to matplotlib plotting method.

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The matplotlib Axes object with the plot.

    See Also
    --------
    plotting.parallel_coordinates : Plot parallel coordinates chart.
    DataFrame.plot : Make plots of Series or DataFrame.

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> df = pd.read_csv(
        ...     "https://raw.githubusercontent.com/pandas-dev/"
        ...     "pandas/main/pandas/tests/io/data/csv/iris.csv"
        ... )  # doctest: +SKIP
        >>> pd.plotting.andrews_curves(df, "Name")  # doctest: +SKIP
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.andrews_curves(
        frame=frame,
        class_column=class_column,
        ax=ax,
        samples=samples,
        color=color,
        colormap=colormap,
        **kwargs,
    )


def andrews_curves(
    frame: DataFrame,
    class_column,
    ax: Axes | None = None,
    samples: int = 200,
    color=None,
    colormap=None,
    **kwds,
) -> Axes:
    import matplotlib.pyplot as plt

    def function(amplitudes):
        def f(t):
            x1 = amplitudes[0]
            result = x1 / np.sqrt(2.0)

            # Take the rest of the coefficients and resize them
            # appropriately. Take a copy of amplitudes as otherwise numpy
            # deletes the element from amplitudes itself.
            coeffs = np.delete(np.copy(amplitudes), 0)
            coeffs = np.resize(coeffs, (int((coeffs.size + 1) / 2), 2))

            # Generate the harmonics and arguments for the sin and cos
            # functions.
            harmonics = np.arange(0, coeffs.shape[0]) + 1
            trig_args = np.outer(harmonics, t)

            result += np.sum(
                coeffs[:, 0, np.newaxis] * np.sin(trig_args)
                + coeffs[:, 1, np.newaxis] * np.cos(trig_args),
                axis=0,
            )
            return result

        return f

    n = len(frame)
    class_col = frame[class_column]
    classes = frame[class_column].drop_duplicates()
    df = frame.drop(class_column, axis=1)
    t = np.linspace(-np.pi, np.pi, samples)
    used_legends: set[str] = set()

    color_values = get_standard_colors(
        num_colors=len(classes), colormap=colormap, color_type="random", color=color
    )
    colors = dict(zip(classes, color_values, strict=False))
    if ax is None:
        ax = plt.gca()
        ax.set_xlim(-np.pi, np.pi)
    for i in range(n):
        row = df.iloc[i].values
        f = function(row)
        y = f(t)
        kls = class_col.iat[i]
        label = pprint_thing(kls)
        if label not in used_legends:
            used_legends.add(label)
            ax.plot(t, y, color=colors[kls], label=label, **kwds)
        else:
            ax.plot(t, y, color=colors[kls], **kwds)

    ax.legend(loc="upper right")
    ax.grid()
    return ax

