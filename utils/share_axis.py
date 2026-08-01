
def share_axis(ax0, ax1, which):
    """Handle changes to post-hoc axis sharing."""
    if _version_predates(mpl, "3.5"):
        group = getattr(ax0, f"get_shared_{which}_axes")()
        group.join(ax1, ax0)
    else:
        getattr(ax1, f"share{which}")(ax0)

