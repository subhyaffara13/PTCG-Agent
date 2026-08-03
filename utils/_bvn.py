import math


def _bvn(a, b, A):
    # covariance matrix is written [[s1**2, rho*s1*s2], [rho*s1*s2, s2**2]]
    # e.g. https://en.wikipedia.org/wiki/Multivariate_normal_distribution
    # therefore, s12 = rho*s1*s2 -> rho = s12/(s1*s2)
    s1 = math.sqrt(A[0, 0])
    s2 = math.sqrt(A[1, 1])
    s12 = A[0, 1]
    r = s12 / (s1 * s2)
    # the x and y coordinates seem to be normalized by the standard devs
    xl, xu = a[0] / s1, b[0] / s1
    yl, yu = a[1] / s2, b[1] / s2
    p = _bvnu(xl, yl, r) - _bvnu(xu, yl, r) - _bvnu(xl, yu, r) + _bvnu(xu, yu, r)
    p = max( 0., min( p, 1. ) )
    return p

