
def truncate(X, lb=-np.inf, ub=np.inf):
    """Truncate the support of a random variable.

    Given a random variable `X`, `truncate` returns a random variable with
    support truncated to the interval between `lb` and `ub`. The underlying
    probability density function is normalized accordingly.

    Parameters
    ----------
    X : `ContinuousDistribution`
        The random variable to be truncated.
    lb, ub : float array-like
        The lower and upper truncation points, respectively. Must be
        broadcastable with one another and the shape of `X`.

    Returns
    -------
    X : `ContinuousDistribution`
        The truncated random variable.

    References
    ----------
    .. [1] "Truncated Distribution". *Wikipedia*.
           https://en.wikipedia.org/wiki/Truncated_distribution

    Examples
    --------
    Compare against `scipy.stats.truncnorm`, which truncates a standard normal,
    *then* shifts and scales it.

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> loc, scale, lb, ub = 1, 2, -2, 2
    >>> X = stats.truncnorm(lb, ub, loc, scale)
    >>> Y = scale * stats.truncate(stats.Normal(), lb, ub) + loc
    >>> x = np.linspace(-3, 5, 300)
    >>> plt.plot(x, X.pdf(x), '-', label='X')
    >>> plt.plot(x, Y.pdf(x), '--', label='Y')
    >>> plt.xlabel('x')
    >>> plt.ylabel('PDF')
    >>> plt.title('Truncated, then Shifted/Scaled Normal')
    >>> plt.legend()
    >>> plt.show()

    However, suppose we wish to shift and scale a normal random variable,
    then truncate its support to given values. This is straightforward with
    `truncate`.

    >>> Z = stats.truncate(scale * stats.Normal() + loc, lb, ub)
    >>> Z.plot()
    >>> plt.show()

    Furthermore, `truncate` can be applied to any random variable:

    >>> Rayleigh = stats.make_distribution(stats.rayleigh)
    >>> W = stats.truncate(Rayleigh(), lb=0.5, ub=3)
    >>> W.plot()
    >>> plt.show()

    """
    return TruncatedDistribution(X, lb=lb, ub=ub)


def truncate(v: Union[str], *, max_len: int = 80) -> str:
    """
    Truncate a value and add a unicode ellipsis (three dots) to the end if it was too long
    """
    warnings.warn('`truncate` is no-longer used by pydantic and is deprecated', DeprecationWarning)
    if isinstance(v, str) and len(v) > (max_len - 2):
        # -3 so quote + string + … + quote has correct length
        return (v[: (max_len - 3)] + '…').__repr__()
    try:
        v = v.__repr__()
    except TypeError:
        v = v.__class__.__repr__(v)  # in case v is a type
    if len(v) > max_len:
        v = v[: max_len - 1] + '…'
    return v

