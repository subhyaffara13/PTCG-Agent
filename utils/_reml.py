
def _reml(lamb, y, order, weights=None):
    """Calculate the restricted maximum likelihood (REML).
    
    Parameters
    ----------
    lamb : penalty
    y : signal
    x : smoothed signal
    order : order of the difference penalty.
    weights : case weights

    Returns
    -------
    reml : REML criterion

    References
    ----------
    - Biessy https://arxiv.org/abs/2306.06932 (version 4)
    - Wood https://doi.org/10.1111/j.1467-9868.2010.00749.x
    """
    n = y.shape[0]
    x, logdet = _solve_WH_banded(
        y=y, lamb=lamb, order=order, weights=weights, calc_logdet=True, warn_user=False
    )
    logdet_DtD = _logdet_difference_matrix(order=order, n=n)
    residual = y - x
    # Eq. 12 of Biessy gives the REML criterion:
    # REML(lambda, sigma) = (log of restriced maximum likelihood)
    #     = -1/2 ((y - theta) W (y - theta) / sigma^2 + lambda theta D'D theta / sigma^2
    #             - log|lambda D'D| + log|(W + lambda D'D)| + (n - p) log(sigma^2)
    #             + const
    #            )
    # where the constant term "const" does not depend on lambda or sigma and p is the
    # order of the difference penalty.
    # Note that Biessy then does not mention to use the profiled REML criterion, i.e.,
    # analytically plug in the optimal sigma^2. This gives us
    #     sigma^2 = r2 / (n - p)
    #     r^2     = (y - theta) W (y - theta) + lambda theta D'D theta
    #     profiled REML(lambda) =
    #         -1/2 (
    #               (n-p) (1 + log(r^2 / (n-p)))
    #               -log|lambda D'D| + log|W + lambda D'D| + const
    #              )
    # This can be compared to Eq. 41 of Bates et al
    # https://doi.org/10.18637/jss.v067.i01.
    # An alternative derivation stems from a mixed model formulation of P-splines, see
    # Currie and Durban https://doi.org/10.1191/1471082x02st039ob or Boer
    # https://doi.org/10.1177/1471082X231178591. One then has 2 variance parameters
    # sigma^2 (from y) and tau^2 (from the random effect) leading to
    #     -1/2 ((y - theta) W (y - theta) / sigma^2 + theta D'D theta / tau^2 + ...
    # One then sets tau^2 = sigma^2 / lambda.
    if weights is None:
        r2 = residual @ residual
    else:
        r2 = residual @ (weights * residual)
    r2 += lamb * np.sum(np.diff(x, n=order)**2)  # + lambda theta D'D theta
    reml = (n - order) * (1 + np.log(r2 / (n - order)))
    reml -= (n - order) * np.log(lamb) + logdet_DtD  # -log|lambda D'D|
    reml += logdet  # +log|W + lambda D'D|
    reml *= -0.5
    return reml

