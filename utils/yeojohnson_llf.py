
def yeojohnson_llf(lmb, data, *, axis=0, nan_policy='propagate', keepdims=False):
    r"""The Yeo-Johnson log-likelihood function.

    Parameters
    ----------
    lmb : scalar
        Parameter for Yeo-Johnson transformation. See `yeojohnson` for
        details.
    data : array_like
        Data to calculate Yeo-Johnson log-likelihood for.
    axis : int, default: 0
        If an int, the axis of the input along which to compute the statistic.
        The statistic of each axis-slice (e.g. row) of the input will appear in a
        corresponding element of the output.
        If ``None``, the input will be raveled before computing the statistic.
    nan_policy : {'propagate', 'omit', 'raise'
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the axis slice (e.g. row) along
          which the  statistic is computed, the corresponding entry of the output
          will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
          If insufficient data remains in the axis slice along which the
          statistic is computed, the corresponding entry of the output will be
          NaN.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    keepdims : bool, default: False
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

    Returns
    -------
    llf : float
        Yeo-Johnson log-likelihood of `data` given `lmb`.

    See Also
    --------
    yeojohnson, probplot, yeojohnson_normplot, yeojohnson_normmax

    Notes
    -----
    The Yeo-Johnson log-likelihood function :math:`l` is defined here as

    .. math::

        l = -\frac{N}{2} \log(\hat{\sigma}^2) + (\lambda - 1)
              \sum_i^N \text{sign}(x_i) \log(|x_i| + 1)

    where :math:`N` is the number of data points :math:`x` = ``data`` and
    :math:`\hat{\sigma}^2` is the estimated variance of the Yeo-Johnson transformed
    input data :math:`x`.
    This corresponds to the *profile log-likelihood* of the original data :math:`x`
    with some constant terms dropped.

    .. versionadded:: 1.2.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    Generate some random variates and calculate Yeo-Johnson log-likelihood
    values for them for a range of ``lmbda`` values:

    >>> x = stats.loggamma.rvs(5, loc=10, size=1000)
    >>> lmbdas = np.linspace(-2, 10)
    >>> llf = np.zeros(lmbdas.shape, dtype=float)
    >>> for ii, lmbda in enumerate(lmbdas):
    ...     llf[ii] = stats.yeojohnson_llf(lmbda, x)

    Also find the optimal lmbda value with `yeojohnson`:

    >>> x_most_normal, lmbda_optimal = stats.yeojohnson(x)

    Plot the log-likelihood as function of lmbda.  Add the optimal lmbda as a
    horizontal line to check that that's really the optimum:

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.plot(lmbdas, llf, 'b.-')
    >>> ax.axhline(stats.yeojohnson_llf(lmbda_optimal, x), color='r')
    >>> ax.set_xlabel('lmbda parameter')
    >>> ax.set_ylabel('Yeo-Johnson log-likelihood')

    Now add some probability plots to show that where the log-likelihood is
    maximized the data transformed with `yeojohnson` looks closest to normal:

    >>> locs = [3, 10, 4]  # 'lower left', 'center', 'lower right'
    >>> for lmbda, loc in zip([-1, lmbda_optimal, 9], locs):
    ...     xt = stats.yeojohnson(x, lmbda=lmbda)
    ...     (osm, osr), (slope, intercept, r_sq) = stats.probplot(xt)
    ...     ax_inset = inset_axes(ax, width="20%", height="20%", loc=loc)
    ...     ax_inset.plot(osm, osr, 'c.', osm, slope*osm + intercept, 'k-')
    ...     ax_inset.set_xticklabels([])
    ...     ax_inset.set_yticklabels([])
    ...     ax_inset.set_title(r'$\lambda=%1.2f$' % lmbda)

    >>> plt.show()

    """
    # _axis_nan_policy decorator does not currently support these for lazy arrays.
    # We want to run tests with lazy backends, so don't pass the arguments explicitly
    # unless necessary.
    kwargs = {}
    if keepdims is not False:
        kwargs['keepdims'] = keepdims
    if nan_policy != 'propagate':
        kwargs['nan_policy'] = nan_policy
    res = _yeojohnson_llf(data, lmb=lmb, axis=axis, **kwargs)
    return res[()] if res.ndim == 0 else res


def yeojohnson_llf(data, lmb, axis=0, _no_deco=False, **kwargs):
    if _no_deco:
        return stats._morestats._yeojohnson_llf(data, lmb=lmb, axis=axis)
    return stats.yeojohnson_llf(lmb, data, axis=axis, **kwargs)

