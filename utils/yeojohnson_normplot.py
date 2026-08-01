
def yeojohnson_normplot(x, la, lb, plot=None, N=80):
    """Compute parameters for a Yeo-Johnson normality plot, optionally show it.

    A Yeo-Johnson normality plot shows graphically what the best
    transformation parameter is to use in `yeojohnson` to obtain a
    distribution that is close to normal.

    Parameters
    ----------
    x : array_like
        Input array.
    la, lb : scalar
        The lower and upper bounds for the ``lmbda`` values to pass to
        `yeojohnson` for Yeo-Johnson transformations. These are also the
        limits of the horizontal axis of the plot if that is generated.
    plot : object, optional
        If given, plots the quantiles and least squares fit.
        `plot` is an object that has to have methods "plot" and "text".
        The `matplotlib.pyplot` module or a Matplotlib Axes object can be used,
        or a custom object with the same methods.
        Default is None, which means that no plot is created.
    N : int, optional
        Number of points on the horizontal axis (equally distributed from
        `la` to `lb`).

    Returns
    -------
    lmbdas : ndarray
        The ``lmbda`` values for which a Yeo-Johnson transform was done.
    ppcc : ndarray
        Probability Plot Correlation Coefficient, as obtained from `probplot`
        when fitting the Box-Cox transformed input `x` against a normal
        distribution.

    See Also
    --------
    probplot, yeojohnson, yeojohnson_normmax, yeojohnson_llf, ppcc_max

    Notes
    -----
    Even if `plot` is given, the figure is not shown or saved by
    `boxcox_normplot`; ``plt.show()`` or ``plt.savefig('figname.png')``
    should be used after calling `probplot`.

    .. versionadded:: 1.2.0

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    Generate some non-normally distributed data, and create a Yeo-Johnson plot:

    >>> x = stats.loggamma.rvs(5, size=500) + 5
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> prob = stats.yeojohnson_normplot(x, -20, 20, plot=ax)

    Determine and plot the optimal ``lmbda`` to transform ``x`` and plot it in
    the same plot:

    >>> _, maxlog = stats.yeojohnson(x)
    >>> ax.axvline(maxlog, color='r')

    >>> plt.show()

    """
    return _normplot('yeojohnson', x, la, lb, plot, N)

