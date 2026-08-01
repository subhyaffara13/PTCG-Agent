
def cgs(A, b, x0=None, *, rtol=1e-5, atol=0., maxiter=None, M=None, callback=None):
    """
    Solve ``Ax = b`` with the Conjugate Gradient Squared method.

    Parameters
    ----------
    A : {sparse array, ndarray, LinearOperator}
        The real-valued N-by-N matrix of the linear system.
        Alternatively, `A` can be a linear operator which can
        produce ``Ax`` using, e.g.,
        ``scipy.sparse.linalg.LinearOperator``.
    b : ndarray
        Right hand side of the linear system. Has shape (N,) or (N,1).
    x0 : ndarray
        Starting guess for the solution.
    rtol, atol : float, optional
        Parameters for the convergence test. For convergence,
        ``norm(b - A @ x) <= max(rtol*norm(b), atol)`` should be satisfied.
        The default is ``atol=0.`` and ``rtol=1e-5``.
    maxiter : int
        Maximum number of iterations.  Iteration will stop after maxiter
        steps even if the specified tolerance has not been achieved.
    M : {sparse array, ndarray, LinearOperator}
        Preconditioner for ``A``. It should approximate the
        inverse of `A` (see Notes). Effective preconditioning dramatically improves the
        rate of convergence, which implies that fewer iterations are needed
        to reach a given error tolerance.
    callback : function
        User-supplied function to call after each iteration.  It is called
        as ``callback(xk)``, where ``xk`` is the current solution vector.

    Returns
    -------
    x : ndarray
        The converged solution.
    info : int
        Provides convergence information:
            0  : successful exit
            >0 : convergence to tolerance not achieved, number of iterations
            <0 : parameter breakdown

    Notes
    -----
    The preconditioner `M` should be a matrix such that ``M @ A`` has a smaller
    condition number than `A`, see [1]_.

    References
    ----------
    .. [1] "Preconditioner", Wikipedia, 
           https://en.wikipedia.org/wiki/Preconditioner
    .. [2] "Conjugate gradient squared", Wikipedia,
           https://en.wikipedia.org/wiki/Conjugate_gradient_squared_method

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import cgs
    >>> R = np.array([[4, 2, 0, 1],
    ...               [3, 0, 0, 2],
    ...               [0, 1, 1, 1],
    ...               [0, 2, 1, 0]])
    >>> A = csc_array(R)
    >>> b = np.array([-1, -0.5, -1, 2])
    >>> x, exit_code = cgs(A, b)
    >>> print(exit_code)  # 0 indicates successful convergence
    0
    >>> np.allclose(A.dot(x), b)
    True
    """
    A, M, x, b = make_system(A, M, x0, b)
    bnrm2 = np.linalg.norm(b)

    atol, _ = _get_atol_rtol('cgs', bnrm2, atol, rtol)

    if bnrm2 == 0:
        return b, 0

    n = len(b)

    dotprod = np.vdot if np.iscomplexobj(x) else np.dot

    if maxiter is None:
        maxiter = n*10

    matvec = A.matvec
    psolve = M.matvec

    rhotol = np.finfo(x.dtype.char).eps**2

    r = b - matvec(x) if x.any() else b.copy()

    rtilde = r.copy()
    bnorm = np.linalg.norm(b)
    if bnorm == 0:
        bnorm = 1

    # Dummy values to initialize vars, silence linter warnings
    rho_prev, p, u, q = None, None, None, None

    for iteration in range(maxiter):
        rnorm = np.linalg.norm(r)
        if rnorm < atol:  # Are we done?
            return x, 0

        rho_cur = dotprod(rtilde, r)
        if np.abs(rho_cur) < rhotol:  # Breakdown case
            return x, -10

        if iteration > 0:
            beta = rho_cur / rho_prev

            # u = r + beta * q
            # p = u + beta * (q + beta * p);
            u[:] = r[:]
            u += beta*q

            p *= beta
            p += q
            p *= beta
            p += u

        else:  # First spin
            p = r.copy()
            u = r.copy()
            q = np.empty_like(r)

        phat = psolve(p)
        vhat = matvec(phat)
        rv = dotprod(rtilde, vhat)

        if rv == 0:  # Dot product breakdown
            return x, -11

        alpha = rho_cur / rv
        q[:] = u[:]
        q -= alpha*vhat
        uhat = psolve(u + q)
        x += alpha*uhat

        # Due to numerical error build-up the actual residual is computed
        # instead of the following two lines that were in the original
        # FORTRAN templates, still using a single matvec.

        # qhat = matvec(uhat)
        # r -= alpha*qhat
        r = b - matvec(x)

        rho_prev = rho_cur

        if callback:
            callback(x)

    else:  # for loop exhausted
        # Return incomplete progress
        return x, maxiter

