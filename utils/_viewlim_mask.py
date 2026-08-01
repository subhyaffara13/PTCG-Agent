
def _viewlim_mask(xs, ys, zs, axes):
    """
    Return the mask of the points outside the axes view limits.

    Parameters
    ----------
    xs, ys, zs : array-like
        The points to mask. These should be in data coordinates.
    axes : Axes3D
        The axes to use for the view limits.

    Returns
    -------
    mask : np.array
        The mask of the points as a bool array.
    """
    mask = np.logical_or.reduce((xs < axes.xy_viewLim.xmin,
                                 xs > axes.xy_viewLim.xmax,
                                 ys < axes.xy_viewLim.ymin,
                                 ys > axes.xy_viewLim.ymax,
                                 zs < axes.zz_viewLim.xmin,
                                 zs > axes.zz_viewLim.xmax))
    return mask

