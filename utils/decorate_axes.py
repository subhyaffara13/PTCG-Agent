
def decorate_axes(ax: Axes, freq: BaseOffset) -> None:
    """Initialize axes for time-series plotting"""
    if not hasattr(ax, "_plot_data"):
        # TODO #54485
        ax._plot_data = []  # type: ignore[attr-defined]

    # TODO #54485
    ax.freq = freq  # type: ignore[attr-defined]
    xaxis = ax.get_xaxis()
    # TODO #54485
    xaxis.freq = freq  # type: ignore[attr-defined]

