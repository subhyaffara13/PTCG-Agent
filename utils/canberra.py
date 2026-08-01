
def canberra(u, v, w=None):
    """
    Compute the Canberra distance between two 1-D arrays.

    The Canberra distance is defined as

    .. math::

         d(u,v) = \\sum_i \\frac{|u_i-v_i|}
                              {|u_i|+|v_i|}.

    Parameters
    ----------
    u : (N,) array_like
        Input array.
    v : (N,) array_like
        Input array.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    canberra : double
        The Canberra distance between vectors `u` and `v`.

    Notes
    -----
    When ``u[i]`` and ``v[i]`` are 0 for given i, then the fraction 0/0 = 0 is
    used in the calculation.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.canberra([1, 0, 0], [0, 1, 0])
    2.0
    >>> distance.canberra([1, 1, 0], [0, 1, 0])
    1.0

    """
    u = _validate_vector(u)
    v = _validate_vector(v, dtype=np.float64)
    if w is not None:
        w = _validate_weights(w)
    with np.errstate(invalid='ignore'):
        abs_uv = abs(u - v)
        abs_u = abs(u)
        abs_v = abs(v)
        d = abs_uv / (abs_u + abs_v)
        if w is not None:
            d = w * d
        d = np.nansum(d)
    return d

