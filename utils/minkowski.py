
def minkowski(u, v, p=2, w=None):
    """
    Compute the Minkowski distance between two arrays.

    The Minkowski distance between arrays `u` and `v`,
    is defined as

    .. math::

       {\\|u-v\\|}_p = (\\sum{|u_i - v_i|^p})^{1/p}.


       \\left(\\sum{w_i(|(u_i - v_i)|^p)}\\right)^{1/p}.

    Parameters
    ----------
    u : (..., N) array_like
        Input array.
    v : (..., N) array_like
        Input array.
    p : scalar
        The order of the norm of the difference :math:`{\\|u-v\\|}_p`. Note
        that for :math:`0 < p < 1`, the triangle inequality only holds with
        an additional multiplicative factor, i.e. it is only a quasi-metric.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    minkowski : float or ndarray
        The Minkowski distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 1)
    2.0
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 2)
    1.4142135623730951
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 3)
    1.2599210498948732
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 1)
    1.0
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 2)
    1.0
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 3)
    1.0

    """
    u = _asarray(u, order='C')
    v = _asarray(v, order='C')
    if p <= 0:
        raise ValueError("p must be greater than 0")
    u_v = u - v
    if w is not None:
        w = _validate_weights(w)
        if p == 1:
            root_w = w
        elif p == 2:
            # better precision and speed
            root_w = np.sqrt(w)
        elif p == np.inf:
            root_w = (w != 0)
        else:
            root_w = np.power(w, 1/p)
        u_v = root_w * u_v
    dist = norm(u_v, ord=p, axis=-1)
    return dist

