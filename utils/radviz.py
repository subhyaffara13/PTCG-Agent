
def radviz(
    frame: DataFrame,
    class_column: str,
    ax: Axes | None = None,
    color: list[str] | tuple[str, ...] | None = None,
    colormap: Colormap | str | None = None,
    **kwds,
) -> Axes:
    """
    Plot a multidimensional dataset in 2D.

    Each Series in the DataFrame is represented as an evenly distributed
    slice on a circle. Each data point is rendered in the circle according to
    the value on each Series. Highly correlated `Series` in the `DataFrame`
    are placed closer on the unit circle.

    RadViz allow to project an N-dimensional data set into a 2D space where the
    influence of each dimension can be interpreted as a balance between the
    influence of all dimensions.

    More info available at the `original article
    <https://doi.org/10.1145/331770.331775>`_
    describing RadViz.

    Parameters
    ----------
    frame : `DataFrame`
        Object holding the data.
    class_column : str
        Column name containing the name of the data point category.
    ax : :class:`matplotlib.axes.Axes`, optional
        A plot instance to which to add the information.
    color : list[str] or tuple[str], optional
        Assign a color to each category. Example: ['blue', 'green'].
    colormap : str or :class:`matplotlib.colors.Colormap`, default None
        Colormap to select colors from. If string, load colormap with that
        name from matplotlib.
    **kwds
        Options to pass to matplotlib scatter plotting method.

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The Axes object from Matplotlib.

    See Also
    --------
    plotting.andrews_curves : Plot clustering visualization.

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> df = pd.DataFrame(
        ...     {
        ...         "SepalLength": [6.5, 7.7, 5.1, 5.8, 7.6, 5.0, 5.4, 4.6, 6.7, 4.6],
        ...         "SepalWidth": [3.0, 3.8, 3.8, 2.7, 3.0, 2.3, 3.0, 3.2, 3.3, 3.6],
        ...         "PetalLength": [5.5, 6.7, 1.9, 5.1, 6.6, 3.3, 4.5, 1.4, 5.7, 1.0],
        ...         "PetalWidth": [1.8, 2.2, 0.4, 1.9, 2.1, 1.0, 1.5, 0.2, 2.1, 0.2],
        ...         "Category": [
        ...             "virginica",
        ...             "virginica",
        ...             "setosa",
        ...             "virginica",
        ...             "virginica",
        ...             "versicolor",
        ...             "versicolor",
        ...             "setosa",
        ...             "virginica",
        ...             "setosa",
        ...         ],
        ...     }
        ... )
        >>> pd.plotting.radviz(df, "Category")  # doctest: +SKIP
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.radviz(
        frame=frame,
        class_column=class_column,
        ax=ax,
        color=color,
        colormap=colormap,
        **kwds,
    )


def radviz(
    frame: DataFrame,
    class_column,
    ax: Axes | None = None,
    color=None,
    colormap=None,
    **kwds,
) -> Axes:
    import matplotlib.pyplot as plt

    def normalize(series):
        a = min(series)
        b = max(series)
        return (series - a) / (b - a)

    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]
    df = frame.drop(class_column, axis=1).apply(normalize)

    if ax is None:
        ax = plt.gca()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)

    to_plot: dict[Hashable, list[list]] = {}
    colors = get_standard_colors(
        num_colors=len(classes), colormap=colormap, color_type="random", color=color
    )

    for kls in classes:
        to_plot[kls] = [[], []]

    m = len(frame.columns) - 1
    s = np.array(
        [(np.cos(t), np.sin(t)) for t in [2 * np.pi * (i / m) for i in range(m)]]
    )

    for i in range(n):
        row = df.iloc[i].values
        row_ = np.repeat(np.expand_dims(row, axis=1), 2, axis=1)
        y = (s * row_).sum(axis=0) / row.sum()
        kls = class_col.iat[i]
        to_plot[kls][0].append(y[0])
        to_plot[kls][1].append(y[1])

    for i, kls in enumerate(classes):
        ax.scatter(
            to_plot[kls][0],
            to_plot[kls][1],
            color=colors[i],
            label=pprint_thing(kls),
            **kwds,
        )
    ax.legend()

    ax.add_patch(mpl.patches.Circle((0.0, 0.0), radius=1.0, facecolor="none"))

    for xy, name in zip(s, df.columns, strict=True):
        ax.add_patch(mpl.patches.Circle(xy, radius=0.025, facecolor="gray"))

        if xy[0] < 0.0 and xy[1] < 0.0:
            ax.text(
                xy[0] - 0.025, xy[1] - 0.025, name, ha="right", va="top", size="small"
            )
        elif xy[0] < 0.0 <= xy[1]:
            ax.text(
                xy[0] - 0.025,
                xy[1] + 0.025,
                name,
                ha="right",
                va="bottom",
                size="small",
            )
        elif xy[1] < 0.0 <= xy[0]:
            ax.text(
                xy[0] + 0.025, xy[1] - 0.025, name, ha="left", va="top", size="small"
            )
        elif xy[0] >= 0.0 and xy[1] >= 0.0:
            ax.text(
                xy[0] + 0.025, xy[1] + 0.025, name, ha="left", va="bottom", size="small"
            )

    ax.axis("equal")
    return ax

