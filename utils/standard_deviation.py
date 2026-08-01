
def standard_deviation(X, condition=None, **kwargs):
    r"""
    Standard Deviation of a random expression

    .. math::
        std(X) = \sqrt(E((X-E(X))^{2}))

    Examples
    ========

    >>> from sympy.stats import Bernoulli, std
    >>> from sympy import Symbol, simplify

    >>> p = Symbol('p')
    >>> B = Bernoulli('B', p, 1, 0)

    >>> simplify(std(B))
    sqrt(p*(1 - p))
    """
    return sqrt(variance(X, condition, **kwargs))


def standard_deviation(input, labels=None, index=None):
    """
    Calculate the standard deviation of the values of an N-D image array,
    optionally at specified sub-regions.

    Parameters
    ----------
    input : array_like
        N-D image data to process.
    labels : array_like, optional
        Labels to identify sub-regions in `input`.
        If not None, must be same shape as `input`.
    index : int or sequence of ints, optional
        `labels` to include in output. If None (default), all values where
        `labels` is non-zero are used.

    Returns
    -------
    standard_deviation : float or ndarray
        Values of standard deviation, for each sub-region if `labels` and
        `index` are specified.

    See Also
    --------
    label, variance, maximum, minimum, extrema

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> from scipy import ndimage
    >>> ndimage.standard_deviation(a)
    2.7585095613392387

    Features to process can be specified using `labels` and `index`:

    >>> lbl, nlbl = ndimage.label(a)
    >>> ndimage.standard_deviation(a, lbl, index=np.arange(1, nlbl+1))
    array([ 1.479,  1.5  ,  3.   ])

    If no index is given, non-zero `labels` are processed:

    >>> ndimage.standard_deviation(a, lbl)
    2.4874685927665499

    """
    return np.sqrt(variance(input, labels, index))

