
def _polynomial_fit(y, lamb, order=2, weights=None, calc_logdet=False):
    """Polynomial fit equivalent to WH for lamb -> infinity."""
    n = len(y)
    x_range = np.arange(n)
    poly = np.polynomial.Polynomial.fit(x=x_range, y=y, deg=order - 1, w=weights)
    if calc_logdet:
        # For large lambda, log|W + lambda D'D| ~ log|lambda D'D|
        # (with determinant understood as product of non-zero eigenvalues). 
        logdet_DtD = _logdet_difference_matrix(order=order, n=n)
        logdet = (n - order) * np.log(lamb) + logdet_DtD
    else:
        logdet = 0.0
    return poly(x_range), logdet

