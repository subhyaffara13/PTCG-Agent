
def _check_ax_limits(col, ax):
    y_min, y_max = ax.get_ylim()
    assert y_min <= col.min()
    assert y_max >= col.max()

