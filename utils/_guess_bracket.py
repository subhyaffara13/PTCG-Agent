
def _guess_bracket(xmin, xmax):
    a = np.full_like(xmin, -1.0)
    b = np.ones_like(xmax)

    i = np.isfinite(xmin) & np.isfinite(xmax)
    a[i] = xmin[i]
    b[i] = xmax[i]

    i = np.isfinite(xmin) & ~np.isfinite(xmax)
    a[i] = xmin[i]
    b[i] = xmin[i] + 1

    i = np.isfinite(xmax) & ~np.isfinite(xmin)
    a[i] = xmax[i] - 1
    b[i] = xmax[i]

    return a, b

