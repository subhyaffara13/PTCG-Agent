
def bicg(A, b, x0=None, *, rtol=1e-5, atol=0., maxiter=None, M=None, callback=None):
    """
    Solve ``Ax = b`` with the BIConjugate Gradient method.

    Parameters
    ----------
    A : {sparse array, ndarray, LinearOperator}
        The real or complex N-by-N matrix of the linear system.
        Alternatively, `A` can be a linear operator which can
        produce ``Ax`` and ``A^T x`` using, e.g.,
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
        Preconditioner for `A`. It should approximate the
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
    condition number than `A`, see [1]_ .

    References
    ----------
    .. [1] "Preconditioner", Wikipedia, 
           https://en.wikipedia.org/wiki/Preconditioner
    .. [2] "Biconjugate gradient method", Wikipedia, 
           https://en.wikipedia.org/wiki/Biconjugate_gradient_method

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import bicg
    >>> A = csc_array([[3, 2, 0], [1, -1, 0], [0, 5, 1.]])
    >>> b = np.array([2., 4., -1.])
    >>> x, exitCode = bicg(A, b, atol=1e-5)
    >>> print(exitCode)  # 0 indicates successful convergence
    0
    >>> np.allclose(A.dot(x), b)
    True
    """
    A, M, x, b = make_system(A, M, x0, b)
    bnrm2 = np.linalg.norm(b)

    atol, _ = _get_atol_rtol('bicg', bnrm2, atol, rtol)

    if bnrm2 == 0:
        return b, 0

    n = len(b)
    dotprod = np.vdot if np.iscomplexobj(x) else np.dot

    if maxiter is None:
        maxiter = n*10

    matvec, rmatvec = A.matvec, A.rmatvec
    psolve, rpsolve = M.matvec, M.rmatvec

    rhotol = np.finfo(x.dtype.char).eps**2

    # Dummy values to initialize vars, silence linter warnings
    rho_prev, p, ptilde = None, None, None

    r = b - matvec(x) if x.any() else b.copy()
    rtilde = r.copy()

    for iteration in range(maxiter):
        if np.linalg.norm(r) < atol:  # Are we done?
            return x, 0

        z = psolve(r)
        ztilde = rpsolve(rtilde)
        # order matters in this dot product
        rho_cur = dotprod(rtilde, z)

        if np.abs(rho_cur) < rhotol:  # Breakdown case
            return x, -10

        if iteration > 0:
            beta = rho_cur / rho_prev
            p *= beta
            p += z
            ptilde *= beta.conj()
            ptilde += ztilde
        else:  # First spin
            p = z.copy()
            ptilde = ztilde.copy()

        q = matvec(p)
        qtilde = rmatvec(ptilde)
        rv = dotprod(ptilde, q)

        if rv == 0:
            return x, -11

        alpha = rho_cur / rv
        x += alpha*p
        r -= alpha*q
        rtilde -= alpha.conj()*qtilde
        rho_prev = rho_cur

        if callback:
            callback(x)

    else:  # for loop exhausted
        # Return incomplete progress
        return x, maxiter

