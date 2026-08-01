
def _scale_invalid_mask(xs, ys, zs, axes):
    """
    Return the mask of points whose coordinates are invalid for the axis
    scale they live on (e.g. <=0 on a log axis).

    Parameters
    ----------
    xs, ys, zs : array-like
        The points to check, in data coordinates.
    axes : Axes3D
        The axes whose scales are queried.

    Returns
    -------
    mask : np.ndarray
        Boolean array, ``True`` where any of x/y/z is out of its scale's
        valid domain.
    """
    return np.logical_or.reduce((
        np.logical_not(axes.xaxis._scale.val_in_range(xs)),
        np.logical_not(axes.yaxis._scale.val_in_range(ys)),
        np.logical_not(axes.zaxis._scale.val_in_range(zs))))

