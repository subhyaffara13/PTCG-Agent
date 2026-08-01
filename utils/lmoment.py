
def lmoment(sample, order=None, *, axis=0, sorted=False, standardize=True):
    r"""Compute L-moments of a sample from a continuous distribution.

    The L-moments of a probability distribution are summary statistics with
    uses similar to those of conventional moments, but they are defined in
    terms of the expected values of order statistics.
    Sample L-moments are defined analogously to population L-moments, and
    they can serve as estimators of population L-moments. They tend to be less
    sensitive to extreme observations than conventional moments.

    Parameters
    ----------
    sample : array_like
        The real-valued sample whose L-moments are desired.
    order : array_like, optional
        The (positive integer) orders of the desired L-moments.
        Must be a scalar or non-empty 1D array. Default is [1, 2, 3, 4].
    axis : int or None, default=0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear
        in a corresponding element of the output. If None, the input will be
        raveled before computing the statistic.
    sorted : bool, default=False
        Whether `sample` is already sorted in increasing order along `axis`.
        If False (default), `sample` will be sorted.
    standardize : bool, default=True
        Whether to return L-moment ratios for orders 3 and higher.
        L-moment ratios are analogous to standardized conventional
        moments: they are the non-standardized L-moments divided
        by the L-moment of order 2.

    Returns
    -------
    lmoments : ndarray
        The sample L-moments of order `order`.

    See Also
    --------
    moment

    Notes
    -----
    SciPy offers only basic capabilities for working with L-moments. For more advanced
    features, consider the ``lmo`` package [4]_.

    References
    ----------
    .. [1] D. Bilkova. "L-Moments and TL-Moments as an Alternative Tool of
           Statistical Data Analysis". Journal of Applied Mathematics and
           Physics. 2014. :doi:`10.4236/jamp.2014.210104`
    .. [2] J. R. M. Hosking. "L-Moments: Analysis and Estimation of Distributions
           Using Linear Combinations of Order Statistics". Journal of the Royal
           Statistical Society. 1990. :doi:`10.1111/j.2517-6161.1990.tb01775.x`
    .. [3] "L-moment". *Wikipedia*. https://en.wikipedia.org/wiki/L-moment.
    .. [4] @jorenham, *Lmo*, https://github.com/jorenham/Lmo/

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng(328458568356392)
    >>> sample = rng.exponential(size=100000)
    >>> stats.lmoment(sample)
    array([1.00124272, 0.50111437, 0.3340092 , 0.16755338])

    Note that the first four standardized population L-moments of the standard
    exponential distribution are 1, 1/2, 1/3, and 1/6; the sample L-moments
    provide reasonable estimates.

    """
    xp = array_namespace(sample)
    args = _lmoment_iv(sample, order, axis, sorted, standardize, xp=xp)
    sample, order, axis, sorted, standardize = args

    n_moments = 4 if is_lazy_array(order) else int(xp.max(order))
    k = xp.arange(n_moments, dtype=sample.dtype)
    prk = _prk(xpx.expand_dims(k, axis=tuple(range(1, sample.ndim+1))), k)
    bk = _br(sample, r=k, xp=xp)

    n = sample.shape[-1]
    if n < bk.shape[-1]:
        bk = xpx.at(bk)[..., n:].set(0)  # remove NaNs due to n_moments > n

    lmoms = xp.vecdot(prk, bk, axis=-1)
    if standardize and n_moments > 2:
        lmoms = xpx.at(lmoms)[2:, ...].divide(lmoms[1, ...])

    if n < lmoms.shape[0]:
        lmoms = xpx.at(lmoms)[n:, ...].set(xp.nan)  # add NaNs where appropriate
    # return lmoms[order-1]  # strict can't handle fancy indexing plus ellipses
    return xp.take(lmoms, order - 1, axis=0) if order.ndim == 1 else lmoms[order - 1]

