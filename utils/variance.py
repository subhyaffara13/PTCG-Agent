
def variance(X, condition=None, **kwargs):
    """
    Variance of a random expression.

    .. math::
        variance(X) = E((X-E(X))^{2})

    Examples
    ========

    >>> from sympy.stats import Die, Bernoulli, variance
    >>> from sympy import simplify, Symbol

    >>> X = Die('X', 6)
    >>> p = Symbol('p')
    >>> B = Bernoulli('B', p, 1, 0)

    >>> variance(2*X)
    35/3

    >>> simplify(variance(B))
    p*(1 - p)
    """
    if is_random(X) and pspace(X) == PSpace():
        from sympy.stats.symbolic_probability import Variance
        return Variance(X, condition)

    return cmoment(X, 2, condition, **kwargs)


def variance(input, labels=None, index=None):
    """
    Calculate the variance of the values of an N-D image array, optionally at
    specified sub-regions.

    Parameters
    ----------
    input : array_like
        Nd-image data to process.
    labels : array_like, optional
        Labels defining sub-regions in `input`.
        If not None, must be same shape as `input`.
    index : int or sequence of ints, optional
        `labels` to include in output.  If None (default), all values where
        `labels` is non-zero are used.

    Returns
    -------
    variance : float or ndarray
        Values of variance, for each sub-region if `labels` and `index` are
        specified.

    See Also
    --------
    label, standard_deviation, maximum, minimum, extrema

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> from scipy import ndimage
    >>> ndimage.variance(a)
    7.609375

    Features to process can be specified using `labels` and `index`:

    >>> lbl, nlbl = ndimage.label(a)
    >>> ndimage.variance(a, lbl, index=np.arange(1, nlbl+1))
    array([ 2.1875,  2.25  ,  9.    ])

    If no index is given, all non-zero `labels` are processed:

    >>> ndimage.variance(a, lbl)
    6.1875

    """
    count, sum, sum_c_sq = _stats(input, labels, index, centered=True)
    return sum_c_sq / np.asanyarray(count).astype(float)

