
def _normplot(method, x, la, lb, plot=None, N=80):
    """Compute parameters for a Box-Cox or Yeo-Johnson normality plot,
    optionally show it.

    See `boxcox_normplot` or `yeojohnson_normplot` for details.
    """

    if method == 'boxcox':
        title = 'Box-Cox Normality Plot'
        transform_func = boxcox
    else:
        title = 'Yeo-Johnson Normality Plot'
        transform_func = yeojohnson

    x = np.asarray(x)
    if x.size == 0:
        return x

    if lb <= la:
        raise ValueError("`lb` has to be larger than `la`.")

    if method == 'boxcox' and np.any(x <= 0):
        raise ValueError("Data must be positive.")

    lmbdas = np.linspace(la, lb, num=N)
    ppcc = lmbdas * 0.0
    for i, val in enumerate(lmbdas):
        # Determine for each lmbda the square root of correlation coefficient
        # of transformed x
        z = transform_func(x, lmbda=val)
        _, (_, _, r) = probplot(z, dist='norm', fit=True)
        ppcc[i] = r

    if plot is not None:
        plot.plot(lmbdas, ppcc, 'x')
        _add_axis_labels_title(plot, xlabel='$\\lambda$',
                               ylabel='Prob Plot Corr. Coef.',
                               title=title)

    return lmbdas, ppcc

