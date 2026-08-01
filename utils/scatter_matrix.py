
def scatter_matrix(
    frame: DataFrame,
    alpha: float = 0.5,
    figsize: tuple[float, float] | None = None,
    ax: Axes | None = None,
    grid: bool = False,
    diagonal: str = "hist",
    marker: str = ".",
    density_kwds: Mapping[str, Any] | None = None,
    hist_kwds: Mapping[str, Any] | None = None,
    range_padding: float = 0.05,
    **kwargs,
) -> np.ndarray:
    """
    Draw a matrix of scatter plots.

    Each pair of numeric columns in the DataFrame is plotted against each other,
    resulting in a matrix of scatter plots. The diagonal plots can display either
    histograms or Kernel Density Estimation (KDE) plots for each variable.

    Parameters
    ----------
    frame : DataFrame
        The data to be plotted.
    alpha : float, optional
        Amount of transparency applied.
    figsize : (float,float), optional
        A tuple (width, height) in inches.
    ax : Matplotlib axis object, optional
        An existing Matplotlib axis object for the plots. If None, a new axis is
        created.
    grid : bool, optional
        Setting this to True will show the grid.
    diagonal : {'hist', 'kde'}
        Pick between 'kde' and 'hist' for either Kernel Density Estimation or
        Histogram plot in the diagonal.
    marker : str, optional
        Matplotlib marker type, default '.'.
    density_kwds : keywords
        Keyword arguments to be passed to kernel density estimate plot.
    hist_kwds : keywords
        Keyword arguments to be passed to hist function.
    range_padding : float, default 0.05
        Relative extension of axis range in x and y with respect to
        (x_max - x_min) or (y_max - y_min).
    **kwargs
        Keyword arguments to be passed to scatter function.

    Returns
    -------
    numpy.ndarray
        A matrix of scatter plots.

    See Also
    --------
    plotting.parallel_coordinates : Plots parallel coordinates for multivariate data.
    plotting.andrews_curves : Generates Andrews curves for visualizing clusters of
        multivariate data.
    plotting.radviz : Creates a RadViz visualization.
    plotting.bootstrap_plot : Visualizes uncertainty in data via bootstrap sampling.

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> df = pd.DataFrame(np.random.randn(1000, 4), columns=["A", "B", "C", "D"])
        >>> pd.plotting.scatter_matrix(df, alpha=0.2)
        array([[<Axes: xlabel='A', ylabel='A'>, <Axes: xlabel='B', ylabel='A'>,
                <Axes: xlabel='C', ylabel='A'>, <Axes: xlabel='D', ylabel='A'>],
               [<Axes: xlabel='A', ylabel='B'>, <Axes: xlabel='B', ylabel='B'>,
                <Axes: xlabel='C', ylabel='B'>, <Axes: xlabel='D', ylabel='B'>],
               [<Axes: xlabel='A', ylabel='C'>, <Axes: xlabel='B', ylabel='C'>,
                <Axes: xlabel='C', ylabel='C'>, <Axes: xlabel='D', ylabel='C'>],
               [<Axes: xlabel='A', ylabel='D'>, <Axes: xlabel='B', ylabel='D'>,
                <Axes: xlabel='C', ylabel='D'>, <Axes: xlabel='D', ylabel='D'>]],
              dtype=object)
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.scatter_matrix(
        frame=frame,
        alpha=alpha,
        figsize=figsize,
        ax=ax,
        grid=grid,
        diagonal=diagonal,
        marker=marker,
        density_kwds=density_kwds,
        hist_kwds=hist_kwds,
        range_padding=range_padding,
        **kwargs,
    )


def scatter_matrix(
    frame: DataFrame,
    alpha: float = 0.5,
    figsize: tuple[float, float] | None = None,
    ax=None,
    grid: bool = False,
    diagonal: str = "hist",
    marker: str = ".",
    density_kwds=None,
    hist_kwds=None,
    range_padding: float = 0.05,
    **kwds,
):
    df = frame._get_numeric_data()
    n = df.columns.size
    naxes = n * n
    fig, axes = create_subplots(naxes=naxes, figsize=figsize, ax=ax, squeeze=False)

    # no gaps between subplots
    maybe_adjust_figure(fig, wspace=0, hspace=0)

    mask = notna(df)

    marker = _get_marker_compat(marker)

    hist_kwds = hist_kwds or {}
    density_kwds = density_kwds or {}

    # GH 14855
    kwds.setdefault("edgecolors", "none")

    boundaries_list = []
    for a in df.columns:
        values = df[a].values[mask[a].values]
        rmin_, rmax_ = np.min(values), np.max(values)
        rdelta_ext = (rmax_ - rmin_) * range_padding / 2
        boundaries_list.append((rmin_ - rdelta_ext, rmax_ + rdelta_ext))

    for i, a in enumerate(df.columns):
        for j, b in enumerate(df.columns):
            ax = axes[i, j]

            if i == j:
                values = df[a].values[mask[a].values]

                # Deal with the diagonal by drawing a histogram there.
                if diagonal == "hist":
                    ax.hist(values, **hist_kwds)

                elif diagonal in ("kde", "density"):
                    from scipy.stats import gaussian_kde

                    y = values
                    gkde = gaussian_kde(y)
                    ind = np.linspace(y.min(), y.max(), 1000)
                    ax.plot(ind, gkde.evaluate(ind), **density_kwds)

                ax.set_xlim(boundaries_list[i])

            else:
                common = (mask[a] & mask[b]).values

                ax.scatter(
                    df[b][common], df[a][common], marker=marker, alpha=alpha, **kwds
                )

                ax.set_xlim(boundaries_list[j])
                ax.set_ylim(boundaries_list[i])

            ax.set_xlabel(b)
            ax.set_ylabel(a)

            if j != 0:
                ax.yaxis.set_visible(False)
            if i != n - 1:
                ax.xaxis.set_visible(False)

    if len(df.columns) > 1:
        lim1 = boundaries_list[0]
        locs = axes[0][1].yaxis.get_majorticklocs()
        locs = locs[(lim1[0] <= locs) & (locs <= lim1[1])]
        adj = (locs - lim1[0]) / (lim1[1] - lim1[0])

        lim0 = axes[0][0].get_ylim()
        adj = adj * (lim0[1] - lim0[0]) + lim0[0]
        axes[0][0].yaxis.set_ticks(adj)

        if np.all(locs == locs.astype(int)):
            # if all ticks are int
            locs = locs.astype(int)
        axes[0][0].yaxis.set_ticklabels(locs)

    set_ticks_props(axes, xlabelsize=8, xrot=90, ylabelsize=8, yrot=0)

    return axes

