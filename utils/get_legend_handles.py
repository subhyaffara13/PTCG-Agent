
def get_legend_handles(legend):
    """Handle legendHandles attribute rename."""
    if _version_predates(mpl, "3.7"):
        return legend.legendHandles
    else:
        return legend.legend_handles

