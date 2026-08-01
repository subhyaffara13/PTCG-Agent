
def sca(ax: Axes) -> None:
    """
    Set the current Axes to *ax* and the current Figure to the parent of *ax*.
    """
    # Mypy sees ax.figure as potentially None,
    # but if you are calling this, it won't be None
    # Additionally the slight difference between `Figure` and `FigureBase` mypy catches
    fig = ax.get_figure(root=False)
    figure(fig)
    fig.sca(ax)  # type: ignore[union-attr]

