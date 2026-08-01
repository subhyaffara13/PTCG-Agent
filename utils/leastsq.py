
def leastsq(func, x0, args=(), Dfun=None, full_output=False,
            col_deriv=False, ftol=1.49012e-8, xtol=1.49012e-8,
            gtol=0.0, maxfev=0, epsfcn=None, factor=100, diag=None):
    """
    Minimize the sum of squares of a set of equations.

    ::

        x = arg min(sum(func(y)**2,axis=0))
                 y

    Parameters
    ----------
    func : callable
        Should take at least one (possibly length ``N`` vector) argument and
        returns ``M`` floating point numbers. It must not return NaNs or
        fitting might fail. ``M`` must be greater than or equal to ``N``.
    x0 : ndarray
        The starting estimate for the minimization.
    args : tuple, optional
        Any extra arguments to func are placed in this tuple.
    Dfun : callable, optional
        A function or method to compute the Jacobian of func with derivatives
        across the rows. If this is None, the Jacobian will be estimated.
    full_output : bool, optional
        If ``True``, return all optional outputs (not just `x` and `ier`).
    col_deriv : bool, optional
        If ``True``, specify that the Jacobian function computes derivatives
        down the columns (faster, because there is no transpose operation).
    ftol : float, optional
        Relative error desired in the sum of squares.
    xtol : float, optional
        Relative error desired in the approximate solution.
    gtol : float, optional
        Orthogonality desired between the function vector and the columns of
        the Jacobian.
    maxfev : int, optional
        The maximum number of calls to the function. If `Dfun` is provided,
        then the default `maxfev` is 100*(N+1) where N is the number of elements
        in x0, otherwise the default `maxfev` is 200*(N+1).
    epsfcn : float, optional
        A variable used in determining a suitable step length for the forward-
        difference approximation of the Jacobian (for Dfun=None).
        Normally the actual step length will be sqrt(epsfcn)*x
        If epsfcn is less than the machine precision, it is assumed that the
        relative errors are of the order of the machine precision.
    factor : float, optional
        A parameter determining the initial step bound
        (``factor * || diag * x||``). Should be in interval ``(0.1, 100)``.
    diag : sequence, optional
        N positive entries that serve as a scale factors for the variables.

    Returns
    -------
    x : ndarray
        The solution (or the result of the last iteration for an unsuccessful
        call).
    cov_x : ndarray
        The inverse of the Hessian. `fjac` and `ipvt` are used to construct an
        estimate of the Hessian. A value of None indicates a singular matrix,
        which means the curvature in parameters `x` is numerically flat. To
        obtain the covariance matrix of the parameters `x`, `cov_x` must be
        multiplied by the variance of the residuals -- see curve_fit. Only
        returned if `full_output` is ``True``.
    infodict : dict
        a dictionary of optional outputs with the keys:

        ``nfev``
            The number of function calls
        ``fvec``
            The function evaluated at the output
        ``fjac``
            A permutation of the R matrix of a QR
            factorization of the final approximate
            Jacobian matrix, stored column wise.
            Together with ipvt, the covariance of the
            estimate can be approximated.
        ``ipvt``
            An integer array of length N which defines
            a permutation matrix, p, such that
            fjac*p = q*r, where r is upper triangular
            with diagonal elements of nonincreasing
            magnitude. Column j of p is column ipvt(j)
            of the identity matrix.
        ``qtf``
            The vector (transpose(q) * fvec).

        Only returned if `full_output` is ``True``.
    mesg : str
        A string message giving information about the cause of failure.
        Only returned if `full_output` is ``True``.
    ier : int
        An integer flag. If it is equal to 1, 2, 3 or 4, the solution was
        found. Otherwise, the solution was not found. In either case, the
        optional output variable 'mesg' gives more information.

    See Also
    --------
    least_squares : Newer interface to solve nonlinear least-squares problems
        with bounds on the variables. See ``method='lm'`` in particular.

    Notes
    -----
    "leastsq" is a wrapper around MINPACK's lmdif and lmder algorithms.

    cov_x is a Jacobian approximation to the Hessian of the least squares
    objective function.
    This approximation assumes that the objective function is based on the
    difference between some observed target data (ydata) and a (non-linear)
    function of the parameters `f(xdata, params)` ::

           func(params) = ydata - f(xdata, params)

    so that the objective function is ::

           min   sum((ydata - f(xdata, params))**2, axis=0)
         params

    The solution, `x`, is always a 1-D array, regardless of the shape of `x0`,
    or whether `x0` is a scalar.

    Examples
    --------
    >>> from scipy.optimize import leastsq
    >>> def func(x):
    ...     return 2*(x-3)**2+1
    >>> leastsq(func, 0)
    (array([2.99999999]), 1)

    """
    x0 = asarray(x0).flatten()
    n = len(x0)
    if not isinstance(args, tuple):
        args = (args,)
    shape, dtype = _check_func('leastsq', 'func', func, x0, args, n)
    m = shape[0]

    if n > m:
        raise TypeError(f"Improper input: func input vector length N={n} must"
                        f" not exceed func output vector length M={m}")

    if epsfcn is None:
        epsfcn = finfo(dtype).eps

    if Dfun is None:
        if maxfev == 0:
            maxfev = 200*(n + 1)
        retval = _minpack._lmdif(func, x0, args, full_output, ftol, xtol,
                                 gtol, maxfev, epsfcn, factor, diag)
    else:
        if col_deriv:
            _check_func('leastsq', 'Dfun', Dfun, x0, args, n, (n, m))
        else:
            _check_func('leastsq', 'Dfun', Dfun, x0, args, n, (m, n))
        if maxfev == 0:
            maxfev = 100 * (n + 1)
        retval = _minpack._lmder(func, Dfun, x0, args, full_output,
                                 col_deriv, ftol, xtol, gtol, maxfev,
                                 factor, diag)

    errors = {0: ["Improper input parameters.", TypeError],
              1: ["Both actual and predicted relative reductions "
                  f"in the sum of squares\n  are at most {ftol:f}", None],
              2: ["The relative error between two consecutive "
                  f"iterates is at most {xtol:f}", None],
              3: ["Both actual and predicted relative reductions in "
                  f"the sum of squares\n  are at most {ftol:f} and the "
                  "relative error between two consecutive "
                  f"iterates is at \n  most {xtol:f}", None],
              4: ["The cosine of the angle between func(x) and any "
                  f"column of the\n  Jacobian is at most {gtol:f} in "
                  "absolute value", None],
              5: ["Number of calls to function has reached "
                  f"maxfev = {maxfev}.", ValueError],
              6: [f"ftol={ftol:f} is too small, no further reduction "
                  "in the sum of squares\n  is possible.",
                  ValueError],
              7: [f"xtol={xtol:f} is too small, no further improvement in "
                  "the approximate\n  solution is possible.",
                  ValueError],
              8: [f"gtol={gtol:f} is too small, func(x) is orthogonal to the "
                  "columns of\n  the Jacobian to machine precision.", ValueError]}

    # The FORTRAN return value (possible return values are >= 0 and <= 8)
    info = retval[-1]

    if full_output:
        cov_x = None
        if info in LEASTSQ_SUCCESS:
            # This was
            # perm = take(eye(n), retval[1]['ipvt'] - 1, 0)
            # r = triu(transpose(retval[1]['fjac'])[:n, :])
            # R = dot(r, perm)
            # cov_x = inv(dot(transpose(R), R))
            # but the explicit dot product was not necessary and sometimes
            # the result was not symmetric positive definite. See gh-4555.
            perm = retval[1]['ipvt']
            n = len(perm)
            r = triu(transpose(retval[1]['fjac'])[:n, :])
            inv_triu = linalg.get_lapack_funcs('trtri', (r,))
            try:
                # inverse of permuted matrix is a permutation of matrix inverse
                invR, trtri_info = inv_triu(r)  # default: upper, non-unit diag
                if trtri_info != 0:  # explicit comparison for readability
                    raise LinAlgError(f'trtri returned info {trtri_info}')
                invR[perm] = invR.copy()
                cov_x = invR @ invR.T
            except (LinAlgError, ValueError):
                pass
        return (retval[0], cov_x) + retval[1:-1] + (errors[info][0], info)
    else:
        if info in LEASTSQ_FAILURE:
            warnings.warn(errors[info][0], RuntimeWarning, stacklevel=2)
        elif info == 0:
            raise errors[info][1](errors[info][0])
        return retval[0], info

