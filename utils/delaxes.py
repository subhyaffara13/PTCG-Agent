
def delaxes(ax: matplotlib.axes.Axes | None = None) -> None:
    """
    Remove an `~.axes.Axes` (defaulting to the current Axes) from its figure.
    """
    if ax is None:
        ax = gca()
    ax.remove()

