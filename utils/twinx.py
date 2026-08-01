
def twinx(ax: matplotlib.axes.Axes | None = None) -> _AxesBase:
    """
    Make and return a second Axes that shares the *x*-axis.  The new Axes will
    overlay *ax* (or the current Axes if *ax* is *None*), and its ticks will be
    on the right.

    Examples
    --------
    :doc:`/gallery/subplots_axes_and_figures/two_scales`
    """
    if ax is None:
        ax = gca()
    ax1 = ax.twinx()
    return ax1

