
def yeojohnson_normmax(x, brack=None, *, nan_policy='propagate'):
    """Compute optimal Yeo-Johnson transform parameter.

    Compute optimal Yeo-Johnson transform parameter for input data, using
    maximum likelihood estimation.

    Parameters
    ----------
    x : array_like
        Input array.
    brack : 2-tuple, optional
        The starting interval for a downhill bracket search with
        `optimize.brent`. Note that this is in most cases not critical; the
        final result is allowed to be outside this bracket. If None,
        `optimize.fminbound` is used with bounds that avoid overflow.
    nan_policy : {'propagate', 'omit', 'raise'}
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the input, the output will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    maxlog : float
        The optimal transform parameter found.

    See Also
    --------
    yeojohnson, yeojohnson_llf, yeojohnson_normplot

    Notes
    -----
    .. versionadded:: 1.2.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    Generate some data and determine optimal ``lmbda``

    >>> rng = np.random.default_rng()
    >>> x = stats.loggamma.rvs(5, size=30, random_state=rng) + 5
    >>> lmax = stats.yeojohnson_normmax(x)

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> prob = stats.yeojohnson_normplot(x, -10, 10, plot=ax)
    >>> ax.axvline(lmax, color='r')

    >>> plt.show()

    """
    def _neg_llf(lmbda, data):
        llf = np.asarray(yeojohnson_llf(lmbda, data))
        # reject likelihoods that are inf which are likely due to small
        # variance in the transformed space
        llf[np.isinf(llf)] = -np.inf
        return -llf

    with np.errstate(invalid='ignore'):
        x = np.asarray(x)

        contains_nan = _contains_nan(x, nan_policy, xp_omit_okay=True)
        if contains_nan:
            if nan_policy == 'propagate':
                return _get_nan(x, xp=np)[()]
            x = x[~np.isnan(x)]  # `nan_policy='omit

        if not np.all(np.isfinite(x)):
            raise ValueError('Yeo-Johnson input must be finite.')
        if np.all(x == 0):
            return 1.0
        if brack is not None:
            return optimize.brent(_neg_llf, brack=brack, args=(x,))

        dtype = x.dtype if np.issubdtype(x.dtype, np.floating) else np.float64
        # Allow values up to 20 times the maximum observed value to be safely
        # transformed without over- or underflow.
        log1p_max_x = np.log1p(20 * np.max(np.abs(x)))
        # Use half of floating point's exponent range to allow safe computation
        # of the variance of the transformed data.
        log_eps = np.log(np.finfo(dtype).eps)
        log_tiny_float = (np.log(np.finfo(dtype).tiny) - log_eps) / 2
        log_max_float = (np.log(np.finfo(dtype).max) + log_eps) / 2
        # Compute the bounds by approximating the inverse of the Yeo-Johnson
        # transform on the smallest and largest floating point exponents, given
        # the largest data we expect to observe. See [1] for further details.
        # [1] https://github.com/scipy/scipy/pull/18852#issuecomment-1630286174
        lb = log_tiny_float / log1p_max_x
        ub = log_max_float / log1p_max_x
        # Convert the bounds if all or some of the data is negative.
        if np.all(x < 0):
            lb, ub = 2 - ub, 2 - lb
        elif np.any(x < 0):
            lb, ub = max(2 - ub, lb), min(2 - lb, ub)
        # Match `optimize.brent`'s tolerance.
        tol_brent = 1.48e-08
        return optimize.fminbound(_neg_llf, lb, ub, args=(x,), xtol=tol_brent)

