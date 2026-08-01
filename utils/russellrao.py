
def russellrao(u, v, w=None):
    """
    Compute the Russell-Rao dissimilarity between two boolean 1-D arrays.

    The Russell-Rao dissimilarity between two boolean 1-D arrays, `u` and
    `v`, is defined as

    .. math::

      \\frac{n - c_{TT}}
           {n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\\mathtt{u[k]} = i` and :math:`\\mathtt{v[k]} = j` for
    :math:`k < n`.

    Parameters
    ----------
    u : (N,) array_like, bool
        Input array.
    v : (N,) array_like, bool
        Input array.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    russellrao : double
        The Russell-Rao dissimilarity between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.russellrao([1, 0, 0], [0, 1, 0])
    1.0
    >>> distance.russellrao([1, 0, 0], [1, 1, 0])
    0.6666666666666666
    >>> distance.russellrao([1, 0, 0], [2, 0, 0])
    0.3333333333333333

    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    if u.dtype == v.dtype == bool and w is None:
        ntt = (u & v).sum()
        n = float(len(u))
    elif w is None:
        ntt = (u * v).sum()
        n = float(len(u))
    else:
        w = _validate_weights(w)
        ntt = (u * v * w).sum()
        n = w.sum()
    return float(n - ntt) / n

