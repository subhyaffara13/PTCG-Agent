
def _get_ax_freq(ax: Axes):
    """
    Get the freq attribute of the ax object if set.
    Also checks shared axes (eg when using secondary yaxis, sharex=True
    or twinx)
    """
    ax_freq = getattr(ax, "freq", None)
    if ax_freq is None:
        # check for left/right ax in case of secondary yaxis
        if hasattr(ax, "left_ax"):
            ax_freq = getattr(ax.left_ax, "freq", None)
        elif hasattr(ax, "right_ax"):
            ax_freq = getattr(ax.right_ax, "freq", None)
    if ax_freq is None:
        # check if a shared ax (sharex/twinx) has already freq set
        shared_axes = ax.get_shared_x_axes().get_siblings(ax)
        if len(shared_axes) > 1:
            for shared_ax in shared_axes:
                ax_freq = getattr(shared_ax, "freq", None)
                if ax_freq is not None:
                    break
    return ax_freq

