
def subplot2grid(
    shape: tuple[int, int], loc: tuple[int, int],
    rowspan: int = 1, colspan: int = 1,
    fig: Figure | None = None,
    **kwargs
) -> matplotlib.axes.Axes:
    """
    Create a subplot at a specific location inside a regular grid.

    Parameters
    ----------
    shape : (int, int)
        Number of rows and of columns of the grid in which to place axis.
    loc : (int, int)
        Row number and column number of the axis location within the grid.
    rowspan : int, default: 1
        Number of rows for the axis to span downwards.
    colspan : int, default: 1
        Number of columns for the axis to span to the right.
    fig : `.Figure`, optional
        Figure to place the subplot in. Defaults to the current figure.
    **kwargs
        Additional keyword arguments are handed to `~.Figure.add_subplot`.

    Returns
    -------
    `~.axes.Axes`

        The Axes of the subplot. The returned Axes can actually be an instance
        of a subclass, such as `.projections.polar.PolarAxes` for polar
        projections.

    Notes
    -----
    The following call ::

        ax = subplot2grid((nrows, ncols), (row, col), rowspan, colspan)

    is identical to ::

        fig = gcf()
        gs = fig.add_gridspec(nrows, ncols)
        ax = fig.add_subplot(gs[row:row+rowspan, col:col+colspan])
    """
    if fig is None:
        fig = gcf()
    rows, cols = shape
    gs = GridSpec._check_gridspec_exists(fig, rows, cols)
    subplotspec = gs.new_subplotspec(loc, rowspan=rowspan, colspan=colspan)
    return fig.add_subplot(subplotspec, **kwargs)

