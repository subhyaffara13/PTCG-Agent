
def _gen_roots_and_weights(n, mu0, an_func, bn_func, f, df, symmetrize, mu):
    """[x,w] = gen_roots_and_weights(n,an_func,sqrt_bn_func,mu)

    Returns the roots (x) of an nth order orthogonal polynomial,
    and weights (w) to use in appropriate Gaussian quadrature with that
    orthogonal polynomial.

    The polynomials have the recurrence relation
          P_n+1(x) = (x - A_n) P_n(x) - B_n P_n-1(x)

    an_func(n)          should return A_n
    sqrt_bn_func(n)     should return sqrt(B_n)
    mu ( = h_0 )        is the integral of the weight over the orthogonal
                        interval
    """
    # lazy import to prevent to prevent linalg dependency for whole module (gh-23420)
    from scipy import linalg
    k = np.arange(n, dtype='d')
    c = np.zeros((2, n))
    c[0,1:] = bn_func(k[1:])
    c[1,:] = an_func(k)
    x = linalg.eigvals_banded(c, overwrite_a_band=True)

    # improve roots by one application of Newton's method
    y = f(n, x)
    dy = df(n, x)
    x -= y/dy

    # fm and dy may contain very large/small values, so we
    # log-normalize them to maintain precision in the product fm*dy
    fm = f(n-1, x)
    log_fm = np.log(np.abs(fm))
    log_dy = np.log(np.abs(dy))
    fm /= np.exp((log_fm.max() + log_fm.min()) / 2.)
    dy /= np.exp((log_dy.max() + log_dy.min()) / 2.)
    w = 1.0 / (fm * dy)

    if symmetrize:
        w = (w + w[::-1]) / 2
        x = (x - x[::-1]) / 2

    w *= mu0 / w.sum()

    if mu:
        return x, w, mu0
    else:
        return x, w

