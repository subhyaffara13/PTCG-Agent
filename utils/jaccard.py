
def jaccard(u, v, w=None):
    r"""
    Compute the Jaccard dissimilarity between two boolean vectors.

    Given boolean vectors :math:`u \equiv (u_1, \cdots, u_n)`
    and :math:`v \equiv (v_1, \cdots, v_n)` that are not both zero,
    their *Jaccard dissimilarity* is defined as ([1]_, p. 26)

    .. math::

       d_\textrm{jaccard}(u, v) := \frac{c_{10} + c_{01}}
                                        {c_{11} + c_{10} + c_{01}}

    where

    .. math::

       c_{ij} := \sum_{1 \le k \le n, u_k=i, v_k=j} 1

    for :math:`i, j \in \{ 0, 1\}`.  If :math:`u` and :math:`v` are both zero,
    their Jaccard dissimilarity is defined to be zero. [2]_

    If a (non-negative) weight vector :math:`w \equiv (w_1, \cdots, w_n)`
    is supplied, the *weighted Jaccard dissimilarity* is defined similarly
    but with :math:`c_{ij}` replaced by

    .. math::

       \tilde{c}_{ij} := \sum_{1 \le k \le n, u_k=i, v_k=j} w_k

    Parameters
    ----------
    u : (N,) array_like of bools
        Input vector.
    v : (N,) array_like of bools
        Input vector.
    w : (N,) array_like of floats, optional
        Weights for each pair of :math:`(u_k, v_k)`.  Default is ``None``,
        which gives each pair a weight of ``1.0``.

    Returns
    -------
    jaccard : float
        The Jaccard dissimilarity between vectors `u` and `v`, optionally
        weighted by `w` if supplied.

    Notes
    -----
    The Jaccard dissimilarity satisfies the triangle inequality and is
    qualified as a metric. [2]_

    The *Jaccard index*, or *Jaccard similarity coefficient*, is equal to
    one minus the Jaccard dissimilarity. [3]_

    The dissimilarity between general (finite) sets may be computed by
    encoding them as boolean vectors and computing the dissimilarity
    between the encoded vectors.
    For example, subsets :math:`A,B` of :math:`\{ 1, 2, ..., n \}` may be
    encoded into boolean vectors :math:`u, v` by setting
    :math:`u_k := 1_{k \in A}`, :math:`v_k := 1_{k \in B}`
    for :math:`k = 1,2,\cdots,n`.

    .. versionchanged:: 1.2.0
       Previously, if all (positively weighted) elements in `u` and `v` are
       zero, the function would return ``nan``.  This was changed to return
       ``0`` instead.

    .. versionchanged:: 1.15.0
       Non-0/1 numeric input used to produce an ad hoc result.  Since 1.15.0,
       numeric input is converted to Boolean before computation.

    References
    ----------
    .. [1] Kaufman, L. and Rousseeuw, P. J.  (1990).  "Finding Groups in Data:
           An Introduction to Cluster Analysis."  John Wiley & Sons, Inc.
    .. [2] Kosub, S.  (2019).  "A note on the triangle inequality for the
           Jaccard distance."  *Pattern Recognition Letters*, 120:36-38.
    .. [3] https://en.wikipedia.org/wiki/Jaccard_index

    Examples
    --------
    >>> from scipy.spatial import distance

    Non-zero vectors with no matching 1s have dissimilarity of 1.0:

    >>> distance.jaccard([1, 0, 0], [0, 1, 0])
    1.0

    Vectors with some matching 1s have dissimilarity less than 1.0:

    >>> distance.jaccard([1, 0, 0, 0], [1, 1, 1, 0])
    0.6666666666666666

    Identical vectors, including zero vectors, have dissimilarity of 0.0:

    >>> distance.jaccard([1, 0, 0], [1, 0, 0])
    0.0
    >>> distance.jaccard([0, 0, 0], [0, 0, 0])
    0.0

    The following example computes the dissimilarity from a confusion matrix
    directly by setting the weight vector to the frequency of True Positive,
    False Negative, False Positive, and True Negative:

    >>> distance.jaccard([1, 1, 0, 0], [1, 0, 1, 0], [31, 41, 59, 26])
    0.7633587786259542  # (41+59)/(31+41+59)

    """
    u = _validate_vector(u)
    v = _validate_vector(v)

    unequal = np.bitwise_xor(u != 0, v != 0)
    nonzero = np.bitwise_or(u != 0, v != 0)
    if w is not None:
        w = _validate_weights(w)
        unequal = w * unequal
        nonzero = w * nonzero
    a = np.float64(unequal.sum())
    b = np.float64(nonzero.sum())
    return (a / b) if b != 0 else np.float64(0)

