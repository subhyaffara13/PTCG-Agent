
def rosen_hess_prod(x, p):
    """
    Product of the Hessian matrix of the Rosenbrock function with a vector.

    Parameters
    ----------
    x : array_like
        1-D array of points at which the Hessian matrix is to be computed.
    p : array_like
        1-D array, the vector to be multiplied by the Hessian matrix.

    Returns
    -------
    rosen_hess_prod : ndarray
        The Hessian matrix of the Rosenbrock function at `x` multiplied
        by the vector `p`.

    See Also
    --------
    rosen, rosen_der, rosen_hess

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize import rosen_hess_prod
    >>> X = 0.1 * np.arange(9)
    >>> p = 0.5 * np.arange(9)
    >>> rosen_hess_prod(X, p)
    array([  -0.,   27.,  -10.,  -95., -192., -265., -278., -195., -180.])

    """
    xp = array_namespace(x, p)
    x = xp_promote(x, force_floating=True, xp=xp)
    x = xpx.atleast_nd(x, ndim=1, xp=xp)
    p = xp.asarray(p, dtype=x.dtype)
    Hp = xp.zeros(x.shape[0], dtype=x.dtype)
    Hp[0] = (1200 * x[0]**2 - 400 * x[1] + 2) * p[0] - 400 * x[0] * p[1]
    Hp[1:-1] = (-400 * x[:-2] * p[:-2] +
                (202 + 1200 * x[1:-1]**2 - 400 * x[2:]) * p[1:-1] -
                400 * x[1:-1] * p[2:])
    Hp[-1] = -400 * x[-2] * p[-2] + 200*p[-1]
    return Hp

