
def _apply_bbox_grid(x, y, Z, bbox):
    """
    Restrict (x, y, Z) to a rectangular bounding box.

    Parameters
    ----------
    x, y : ndarray
        Monotonic sample coordinates.
    Z : ndarray, shape (len(x), len(y))
        Data grid.
    bbox : sequence of 4 scalars or None
        ``(xb, xe, yb, ye)``; any element may be None to skip clipping.

    Returns
    -------
    x_fit, y_fit, Z_fit : ndarray
        Sliced arrays restricted to bbox.
    ix, iy : slice or ndarray
        Indexers mapping from full arrays to the restricted ones.

    Raises
    ------
    ValueError
        If bbox is invalid or excludes all samples along an axis.
    """
    if all([bboxi is None for bboxi in bbox]):
        return x, y, Z, slice(None), slice(None)

    xb, xe, yb, ye = bbox
    if not (xb < xe and yb < ye):
        raise ValueError("bbox must satisfy xb < xe and yb < ye")

    ix = np.where((x >= xb) & (x <= xe))[0]
    iy = np.where((y >= yb) & (y <= ye))[0]
    if ix.size == 0 or iy.size == 0:
        raise ValueError("bbox excludes all samples in x or y.")

    return x[ix], y[iy], Z[np.ix_(ix, iy)], np.s_[ix], np.s_[iy]

