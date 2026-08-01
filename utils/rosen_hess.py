
def rosen_hess(x):
    """
    The Hessian matrix of the Rosenbrock function.

    Parameters
    ----------
    x : array_like
        1-D array of points at which the Hessian matrix is to be computed.

    Returns
    -------
    rosen_hess : ndarray
        The Hessian matrix of the Rosenbrock function at `x`.

    See Also
    --------
    rosen, rosen_der, rosen_hess_prod

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize import rosen_hess
    >>> X = 0.1 * np.arange(4)
    >>> rosen_hess(X)
    array([[-38.,   0.,   0.,   0.],
           [  0., 134., -40.,   0.],
           [  0., -40., 130., -80.],
           [  0.,   0., -80., 200.]])

    """
    xp = array_namespace(x)
    x = xp_promote(x, force_floating=True, xp=xp)

    H = (xpx.create_diagonal(-400 * x[:-1], offset=1, xp=xp)
         - xpx.create_diagonal(400 * x[:-1], offset=-1, xp=xp))
    diagonal = xp.zeros(x.shape[0], dtype=x.dtype)
    diagonal = xpx.at(diagonal)[0].set(1200 * x[0]**2 - 400 * x[1] + 2)
    diagonal = xpx.at(diagonal)[-1].set(200)
    diagonal = xpx.at(diagonal)[1:-1].set(202 + 1200 * x[1:-1]**2 - 400 * x[2:])
    return H + xpx.create_diagonal(diagonal, xp=xp)

