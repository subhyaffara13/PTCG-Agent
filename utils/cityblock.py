
def cityblock(u, v, w=None):
    """
    Compute the City Block (Manhattan) distance.

    Computes the Manhattan distance between two 1-D arrays `u` and `v`,
    which is defined as

    .. math::

       \\sum_i {\\left| u_i - v_i \\right|}.

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
    cityblock : double
        The City Block (Manhattan) distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.cityblock([1, 0, 0], [0, 1, 0])
    2
    >>> distance.cityblock([1, 0, 0], [0, 2, 0])
    3
    >>> distance.cityblock([1, 0, 0], [1, 1, 0])
    1

    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    l1_diff = abs(u - v)
    if w is not None:
        w = _validate_weights(w)
        l1_diff = w * l1_diff
    return l1_diff.sum()

