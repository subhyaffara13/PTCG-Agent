
def kurtosis(X, condition=None, **kwargs):
    r"""
    Characterizes the tails/outliers of a probability distribution.

    Explanation
    ===========

    Kurtosis of any univariate normal distribution is 3. Kurtosis less than
    3 means that the distribution produces fewer and less extreme outliers
    than the normal distribution.

    .. math::
        kurtosis(X) = E(((X - E(X))/\sigma_X)^{4})

    Parameters
    ==========

    condition : Expr containing RandomSymbols
            A conditional expression. kurtosis(X, X>0) is kurtosis of X given X > 0

    Examples
    ========

    >>> from sympy.stats import kurtosis, Exponential, Normal
    >>> from sympy import Symbol
    >>> X = Normal('X', 0, 1)
    >>> kurtosis(X)
    3
    >>> kurtosis(X, X > 0) # find kurtosis given X > 0
    (-4/pi - 12/pi**2 + 3)/(1 - 2/pi)**2

    >>> rate = Symbol('lamda', positive=True, real=True)
    >>> Y = Exponential('Y', rate)
    >>> kurtosis(Y)
    9

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kurtosis
    .. [2] https://mathworld.wolfram.com/Kurtosis.html
    """
    return smoment(X, 4, condition=condition, **kwargs)


def kurtosis(a, axis=0, fisher=True, bias=True):
    """
    Computes the kurtosis (Fisher or Pearson) of a dataset.

    Kurtosis is the fourth central moment divided by the square of the
    variance. If Fisher's definition is used, then 3.0 is subtracted from
    the result to give 0.0 for a normal distribution.

    If bias is False then the kurtosis is calculated using k statistics to
    eliminate bias coming from biased moment estimators

    Use `kurtosistest` to see if result is close enough to normal.

    Parameters
    ----------
    a : array
        data for which the kurtosis is calculated
    axis : int or None, optional
        Axis along which the kurtosis is calculated. Default is 0.
        If None, compute over the whole array `a`.
    fisher : bool, optional
        If True, Fisher's definition is used (normal ==> 0.0). If False,
        Pearson's definition is used (normal ==> 3.0).
    bias : bool, optional
        If False, then the calculations are corrected for statistical bias.

    Returns
    -------
    kurtosis : array
        The kurtosis of values along an axis. If all values are equal,
        return -3 for Fisher's definition and 0 for Pearson's definition.

    Notes
    -----
    For more details about `kurtosis`, see `scipy.stats.kurtosis`.

    """
    a, axis = _chk_asarray(a, axis)
    mean = a.mean(axis, keepdims=True)
    m2 = _moment(a, 2, axis, mean=mean)
    m4 = _moment(a, 4, axis, mean=mean)
    zero = (m2 <= (np.finfo(m2.dtype).resolution * mean.squeeze(axis))**2)
    with np.errstate(all='ignore'):
        vals = ma.where(zero, 0, m4 / m2**2.0)

    if not bias and zero is not ma.masked and m2 is not ma.masked:
        n = a.count(axis)
        can_correct = ~zero & (n > 3)
        if can_correct.any():
            n = np.extract(can_correct, n)
            m2 = np.extract(can_correct, m2)
            m4 = np.extract(can_correct, m4)
            nval = 1.0/(n-2)/(n-3)*((n*n-1.0)*m4/m2**2.0-3*(n-1)**2.0)
            np.place(vals, can_correct, nval+3.0)
    if fisher:
        return vals - 3
    else:
        return vals


def kurtosis(a, axis=0, fisher=True, bias=True, nan_policy='propagate'):
    """Compute the kurtosis (Fisher or Pearson) of a dataset.

    Kurtosis is the fourth central moment divided by the square of the
    variance. If Fisher's definition is used, then 3.0 is subtracted from
    the result to give 0.0 for a normal distribution.

    If bias is False then the kurtosis is calculated using k statistics to
    eliminate bias coming from biased moment estimators

    Use `kurtosistest` to see if result is close enough to normal.

    Parameters
    ----------
    a : array
        Data for which the kurtosis is calculated.
    axis : int or None, optional
        Axis along which the kurtosis is calculated. Default is 0.
        If None, compute over the whole array `a`.
    fisher : bool, optional
        If True, Fisher's definition is used (normal ==> 0.0). If False,
        Pearson's definition is used (normal ==> 3.0).
    bias : bool, optional
        If False, then the calculations are corrected for statistical bias.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.

    Returns
    -------
    kurtosis : array
        The kurtosis of values along an axis, returning NaN where all values
        are equal.

    References
    ----------
    .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.

    Examples
    --------
    In Fisher's definition, the kurtosis of the normal distribution is zero.
    In the following example, the kurtosis is close to zero, because it was
    calculated from the dataset, not from the continuous distribution.

    >>> import numpy as np
    >>> from scipy.stats import norm, kurtosis
    >>> data = norm.rvs(size=1000, random_state=3)
    >>> kurtosis(data)
    -0.06928694200380558

    The distribution with a higher kurtosis has a heavier tail.
    The zero valued kurtosis of the normal distribution in Fisher's definition
    can serve as a reference point.

    >>> import matplotlib.pyplot as plt
    >>> import scipy.stats as stats
    >>> from scipy.stats import kurtosis

    >>> x = np.linspace(-5, 5, 100)
    >>> ax = plt.subplot()
    >>> distnames = ['laplace', 'norm', 'uniform']

    >>> for distname in distnames:
    ...     if distname == 'uniform':
    ...         dist = getattr(stats, distname)(loc=-2, scale=4)
    ...     else:
    ...         dist = getattr(stats, distname)
    ...     data = dist.rvs(size=1000)
    ...     kur = kurtosis(data, fisher=True)
    ...     y = dist.pdf(x)
    ...     ax.plot(x, y, label="{}, {}".format(distname, round(kur, 3)))
    ...     ax.legend()

    The Laplace distribution has a heavier tail than the normal distribution.
    The uniform distribution (which has negative kurtosis) has the thinnest
    tail.

    """
    xp = array_namespace(a)
    a, axis = _chk_asarray(a, axis, xp=xp)

    n = _count_nonmasked(a, axis, xp=xp)
    mean = xp.mean(a, axis=axis, keepdims=True)
    mean_reduced = xp.squeeze(mean, axis=axis)  # needed later
    m2 = _moment(a, 2, axis, center=mean, xp=xp)
    m4 = _moment(a, 4, axis, center=mean, xp=xp)
    with np.errstate(all='ignore'):
        zero = m2 <= (xp.finfo(m2.dtype).eps * mean_reduced)**2
        vals = xp.where(zero, xp.nan, m4 / m2**2.0)

    if not bias:
        can_correct = ~zero & (n > 3)
        if is_lazy_array(can_correct) or xp.any(can_correct):
            nval = 1.0/(n-2)/(n-3) * ((n**2-1.0)*m4/m2**2.0 - 3*(n-1)**2.0)
            vals = xp.where(can_correct, nval + 3.0, vals)

    vals = vals - 3 if fisher else vals
    return vals[()] if vals.ndim == 0 else vals

