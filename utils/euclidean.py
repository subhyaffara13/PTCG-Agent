
def euclidean(u, v, w=None):
    """
    Computes the Euclidean distance between two arrays.

    The Euclidean distance between arrays `u` and `v`, is defined as

    .. math::

       {\\|u-v\\|}_2

       \\left(\\sum{(w_i |(u_i - v_i)|^2)}\\right)^{1/2}

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
    euclidean : float or ndarray
        The Euclidean distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.euclidean([1, 0, 0], [0, 1, 0])
    1.4142135623730951
    >>> distance.euclidean([1, 1, 0], [0, 1, 0])
    1.0

    """
    return minkowski(u, v, p=2, w=w)

