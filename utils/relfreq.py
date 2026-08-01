
def relfreq(a, numbins=10, defaultreallimits=None, weights=None):
    """Return a relative frequency histogram, using the histogram function.

    A relative frequency  histogram is a mapping of the number of
    observations in each of the bins relative to the total of observations.

    Parameters
    ----------
    a : array_like
        Input array.
    numbins : int, optional
        The number of bins to use for the histogram. Default is 10.
    defaultreallimits : tuple (lower, upper), optional
        The lower and upper values for the range of the histogram.
        If no value is given, a range slightly larger than the range of the
        values in a is used. Specifically ``(a.min() - s, a.max() + s)``,
        where ``s = (1/2)(a.max() - a.min()) / (numbins - 1)``.
    weights : array_like, optional
        The weights for each value in `a`. Default is None, which gives each
        value a weight of 1.0

    Returns
    -------
    frequency : ndarray
        Binned values of relative frequency.
    lowerlimit : float
        Lower real limit.
    binsize : float
        Width of each bin.
    extrapoints : int
        Extra points.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats
    >>> rng = np.random.default_rng()
    >>> a = np.array([2, 4, 1, 2, 3, 2])
    >>> res = stats.relfreq(a, numbins=4)
    >>> res.frequency
    array([ 0.16666667, 0.5       , 0.16666667,  0.16666667])
    >>> np.sum(res.frequency)  # relative frequencies should add up to 1
    1.0

    Create a normal distribution with 1000 random values

    >>> samples = stats.norm.rvs(size=1000, random_state=rng)

    Calculate relative frequencies

    >>> res = stats.relfreq(samples, numbins=25)

    Calculate space of values for x

    >>> x = res.lowerlimit + np.linspace(0, res.binsize*res.frequency.size,
    ...                                  res.frequency.size)

    Plot relative frequency histogram

    >>> fig = plt.figure(figsize=(5, 4))
    >>> ax = fig.add_subplot(1, 1, 1)
    >>> ax.bar(x, res.frequency, width=res.binsize)
    >>> ax.set_title('Relative frequency histogram')
    >>> ax.set_xlim([x.min(), x.max()])

    >>> plt.show()

    """
    h, l, b, e = _histogram(a, numbins, defaultreallimits, weights=weights,
                            density=True)
    return RelfreqResult(h, l, b, e)

