
def yeojohnson(x, lmbda=None, *, nan_policy='propagate'):
    r"""Return a dataset transformed by a Yeo-Johnson power transformation.

    Parameters
    ----------
    x : ndarray
        Input array.  Should be 1-dimensional.
    lmbda : float, optional
        If ``lmbda`` is ``None``, find the lambda that maximizes the
        log-likelihood function and return it as the second output argument.
        Otherwise the transformation is done for the given value.
    nan_policy : {'propagate', 'omit', 'raise'}
        Defines how to handle NaNs in `x`.

        - ``propagate``: if a NaN is present, all outputs will contain NaNs.
        - ``omit``: NaNs will be omitted when calculating the optimal `maxlog`;
           NaNs in `x` will remain NaNs in the transformed data.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    yeojohnson: ndarray
        Yeo-Johnson power transformed array.
    maxlog : float, optional
        If the `lmbda` parameter is None, the second returned argument is
        the lambda that maximizes the log-likelihood function.

    See Also
    --------
    probplot, yeojohnson_normplot, yeojohnson_normmax, yeojohnson_llf, boxcox

    Notes
    -----
    The Yeo-Johnson transform is given by:

    .. math::

        y =
        \begin{cases}
        \frac{(x + 1)^\lambda - 1}{\lambda},
        &\text{for } x \geq 0, \lambda \neq 0
        \\
        \log(x + 1),
        &\text{for } x \geq 0, \lambda = 0
        \\
        -\frac{(-x + 1)^{2 - \lambda} - 1}{2 - \lambda},
        &\text{for } x < 0, \lambda \neq 2
        \\
        -\log(-x + 1),
        &\text{for } x < 0, \lambda = 2
        \end{cases}

    Unlike `boxcox`, `yeojohnson` does not require the input data to be
    positive.

    .. versionadded:: 1.2.0


    References
    ----------
    I. Yeo and R.A. Johnson, "A New Family of Power Transformations to
    Improve Normality or Symmetry", Biometrika 87.4 (2000):


    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    We generate some random variates from a non-normal distribution and make a
    probability plot for it, to show it is non-normal in the tails:

    >>> fig = plt.figure()
    >>> ax1 = fig.add_subplot(211)
    >>> x = stats.loggamma.rvs(5, size=500) + 5
    >>> prob = stats.probplot(x, dist=stats.norm, plot=ax1)
    >>> ax1.set_xlabel('')
    >>> ax1.set_title('Probplot against normal distribution')

    We now use `yeojohnson` to transform the data so it's closest to normal:

    >>> ax2 = fig.add_subplot(212)
    >>> xt, lmbda = stats.yeojohnson(x)
    >>> prob = stats.probplot(xt, dist=stats.norm, plot=ax2)
    >>> ax2.set_title('Probplot after Yeo-Johnson transformation')

    >>> plt.show()

    """
    x = np.asarray(x)
    if x.size == 0:
        return x

    if np.issubdtype(x.dtype, np.complexfloating):
        raise ValueError('Yeo-Johnson transformation is not defined for '
                         'complex numbers.')

    if np.issubdtype(x.dtype, np.integer):
        x = x.astype(np.float64, copy=False)

    if lmbda is not None:
        _contains_nan(x, nan_policy, xp_omit_okay=True)  # handle nan_policy='raise'
        return _yeojohnson_transform(x, lmbda)

    # if lmbda=None, find the lmbda that maximizes the log-likelihood function.
    lmax = yeojohnson_normmax(x, nan_policy=nan_policy)
    y = _yeojohnson_transform(x, lmax)

    return y, lmax

