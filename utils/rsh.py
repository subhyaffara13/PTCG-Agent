
def rsh(data, points=None):
    """
    Evaluates Rosenblatt's shifted histogram estimators for each data point.

    Rosenblatt's estimator is a centered finite-difference approximation to the
    derivative of the empirical cumulative distribution function.

    Parameters
    ----------
    data : sequence
        Input data, should be 1-D. Masked values are ignored.
    points : sequence or None, optional
        Sequence of points where to evaluate Rosenblatt shifted histogram.
        If None, use the data.

    """  # numpydoc ignore=RT01
    data = ma.array(data, copy=False)
    if points is None:
        points = data
    else:
        points = np.atleast_1d(np.asarray(points))

    if data.ndim != 1:
        raise AttributeError("The input array should be 1D only !")

    n = data.count()
    r = idealfourths(data, axis=None)
    h = 1.2 * (r[-1]-r[0]) / n**(1./5)
    nhi = (data[:,None] <= points[None,:] + h).sum(0)
    nlo = (data[:,None] < points[None,:] - h).sum(0)
    return (nhi-nlo) / (2.*n*h)

