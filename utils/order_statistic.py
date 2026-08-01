
def order_statistic(X, /, *, r, n):
    r"""Probability distribution of an order statistic.

    Returns a random variable that follows the distribution of the
    :math:`r^{\text{th}}` order statistic of a sample of :math:`n`
    observations of a random variable :math:`X`.

    Parameters
    ----------
    X : `ContinuousDistribution`
        The random variable :math:`X`.
    r : array_like
        The (positive integer) rank of the order statistic :math:`r`,
        satisfying ``1 <= r <= n``.
    n : array_like
        The (positive integer) sample size :math:`n`.

    Returns
    -------
    Y : `ContinuousDistribution`
        A random variable that follows the distribution of the prescribed
        order statistic.

    Notes
    -----
    If we make :math:`n` observations of a continuous random variable
    :math:`X` and sort them in increasing order
    :math:`X_{(1)}, \dots, X_{(r)}, \dots, X_{(n)}`, then :math:`X_{(r)}`
    is known as the :math:`r^{\text{th}}` order statistic.

    If the PDF, CDF, and CCDF of :math:`X` are denoted by :math:`f`,
    :math:`F`, and :math:`G = 1 - F`, respectively, then the PDF of
    :math:`X_{(r)}` is given by:

    .. math::

        f_r(x) = \frac{n!}{(r-1)! (n-r)!} f(x) F(x)^{r-1} G(x)^{n - r}

    The CDF and other methods of the distribution of :math:`X_{(r)}`
    are calculated using the fact that :math:`X = F^{-1}(U)`, where :math:`U` is a
    standard uniform random variable, together with the fact that the order statistics
    of i.i.d. uniform random variables follow a beta distribution
    :math:`B(r, n - r + 1)`.

    References
    ----------
    .. [1] Order statistic. *Wikipedia*. https://en.wikipedia.org/wiki/Order_statistic

    Examples
    --------
    Suppose we are interested in order statistics of samples of size five drawn
    from the standard normal distribution. Plot the PDF of each
    order statistic and compare with a normalized histogram from simulation.

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>>
    >>> X = stats.Normal()
    >>> data = X.sample(shape=(10000, 5))
    >>> sorted_data = np.sort(data, axis=1)
    >>> Y = stats.order_statistic(X, r=[1, 2, 3, 4, 5], n=5)
    >>>
    >>> ax = plt.gca()
    >>> colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    >>> for i in range(5):
    ...     y = sorted_data[:, i]
    ...     ax.hist(y, density=True, bins=30, alpha=0.1, color=colors[i])
    >>> Y.plot(ax=ax)
    >>> plt.show()

    """
    r, n = np.asarray(r), np.asarray(n)
    if np.any((r != np.floor(r)) | (r < 0)) or np.any((n != np.floor(n)) | (n < 0)):
        message = "`r` and `n` must contain only positive integers."
        raise ValueError(message)
    return OrderStatisticDistribution(X, r=r, n=n)

