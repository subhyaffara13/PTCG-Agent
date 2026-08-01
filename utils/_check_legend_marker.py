
def _check_legend_marker(ax, expected_markers=None, visible=True):
    """
    Check ax has expected legend markers

    Parameters
    ----------
    ax : matplotlib Axes object
    expected_markers : list-like
        expected legend markers
    visible : bool
        expected legend visibility. labels are checked only when visible is
        True
    """
    if visible and (expected_markers is None):
        raise ValueError("Markers must be specified when visible is True")
    if visible:
        handles, _ = ax.get_legend_handles_labels()
        markers = [handle.get_marker() for handle in handles]
        assert markers == expected_markers
    else:
        assert ax.get_legend() is None

