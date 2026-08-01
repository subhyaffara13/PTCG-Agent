
def sqeuclidean(u, v, w=None):
    """
    Compute the squared Euclidean distance between two arrays.

    The squared Euclidean distance between `u` and `v` is defined as

    .. math::

       \\sum_i{w_i |u_i - v_i|^2}

    Parameters
    ----------
    u : (..., N) array_like
        Input array.
    v : (..., N) array_like
        Input array.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    sqeuclidean : float or ndarray
        The squared Euclidean distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.sqeuclidean([1, 0, 0], [0, 1, 0])
    2.0
    >>> distance.sqeuclidean([1, 1, 0], [0, 1, 0])
    1.0

    """
    # Preserve float dtypes, but convert everything else to np.float64
    # for stability.
    utype, vtype = None, None
    if not (hasattr(u, "dtype") and np.issubdtype(u.dtype, np.inexact)):
        utype = np.float64
    if not (hasattr(v, "dtype") and np.issubdtype(v.dtype, np.inexact)):
        vtype = np.float64

    u = _asarray(u, dtype=utype, order='C')
    v = _asarray(v, dtype=vtype, order='C')
    u_v = u - v
    u_v_w = u_v  # only want weights applied once
    if w is not None:
        w = _validate_weights(w)
        u_v_w = w * u_v
    return np.vecdot(u_v, u_v_w)

