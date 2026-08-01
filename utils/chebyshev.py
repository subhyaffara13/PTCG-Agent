
def chebyshev(u, v, w=None):
    r"""
    Compute the Chebyshev distance.

    The *Chebyshev distance* between real vectors
    :math:`u \equiv (u_1, \cdots, u_n)` and
    :math:`v \equiv (v_1, \cdots, v_n)` is defined as [1]_

    .. math::

       d_\textrm{chebyshev}(u,v) := \max_{1 \le i \le n} |u_i-v_i|

    If a (non-negative) weight vector :math:`w \equiv (w_1, \cdots, w_n)`
    is supplied, the *weighted Chebyshev distance* is defined to be the
    weighted Minkowski distance of infinite order; that is,

    .. math::

       \begin{align}
       d_\textrm{chebyshev}(u,v;w) &:= \lim_{p\rightarrow \infty}
          \left( \sum_{i=1}^n w_i | u_i-v_i |^p \right)^\frac{1}{p} \\
        &= \max_{1 \le i \le n} 1_{w_i > 0} | u_i - v_i |
       \end{align}

    Parameters
    ----------
    u : (N,) array_like of floats
        Input vector.
    v : (N,) array_like of floats
        Input vector.
    w : (N,) array_like of floats, optional
        Weight vector.  Default is ``None``, which gives all pairs
        :math:`(u_i, v_i)` the same weight ``1.0``.

    Returns
    -------
    chebyshev : float
        The Chebyshev distance between vectors `u` and `v`, optionally weighted
        by `w`.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chebyshev_distance

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.chebyshev([1, 0, 0], [0, 1, 0])
    1
    >>> distance.chebyshev([1, 1, 0], [0, 1, 0])
    1

    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    if w is not None:
        w = _validate_weights(w)
        return max((w > 0) * abs(u - v))
    return max(abs(u - v))

