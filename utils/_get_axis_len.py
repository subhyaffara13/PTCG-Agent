
def _get_axis_len(aname, a, axis):
    ax = axis
    if ax < 0:
        ax += a.ndim
    if 0 <= ax < a.ndim:
        return a.shape[ax]
    raise ValueError(f"'{aname}axis' entry is out of bounds")

