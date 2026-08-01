
def check_gradient(fcn, Dfcn, x0, args=(), col_deriv=False):
    """Perform a simple check on the gradient for correctness.

    """

    x = atleast_1d(x0)
    n = len(x)
    x = x.reshape((n,))
    fvec = atleast_1d(fcn(x, *args))
    m = len(fvec)
    fvec = fvec.reshape((m,))
    ldfjac = m
    fjac = atleast_1d(Dfcn(x, *args))
    fjac = fjac.reshape((m, n))
    if not col_deriv:
        fjac = transpose(fjac)

    xp = zeros((n,), float)
    err = zeros((m,), float)
    fvecp = None
    _minpack._chkder(m, n, x, fvec, fjac, ldfjac, xp, fvecp, 1, err)

    fvecp = atleast_1d(fcn(xp, *args))
    fvecp = fvecp.reshape((m,))
    _minpack._chkder(m, n, x, fvec, fjac, ldfjac, xp, fvecp, 2, err)

    good = (prod(greater(err, 0.5), axis=0))

    return (good, err)

