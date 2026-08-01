
def bicgstab(A, b, x0=None, *, rtol=1e-5, atol=0., maxiter=None, M=None,
             callback=None):
    """
    Solve ``Ax = b`` with the BIConjugate Gradient STABilized method.

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
    .. [2] "Biconjugate gradient stabilized method", 
           Wikipedia, https://en.wikipedia.org/wiki/Biconjugate_gradient_stabilized_method

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import bicgstab
    >>> R = np.array([[4, 2, 0, 1],
    ...               [3, 0, 0, 2],
    ...               [0, 1, 1, 1],
    ...               [0, 2, 1, 0]])
    >>> A = csc_array(R)
    >>> b = np.array([-1, -0.5, -1, 2])
    >>> x, exit_code = bicgstab(A, b, atol=1e-5)
    >>> print(exit_code)  # 0 indicates successful convergence
    0
    >>> np.allclose(A.dot(x), b)
    True
    """
    A, M, x, b = make_system(A, M, x0, b)
    bnrm2 = np.linalg.norm(b)

    atol, _ = _get_atol_rtol('bicgstab', bnrm2, atol, rtol)

    if bnrm2 == 0:
        return b, 0

    n = len(b)

    dotprod = np.vdot if np.iscomplexobj(x) else np.dot

    if maxiter is None:
        maxiter = n*10

    matvec = A.matvec
    psolve = M.matvec

    # These values make no sense but coming from original Fortran code
    # sqrt might have been meant instead.
    rhotol = np.finfo(x.dtype.char).eps**2
    omegatol = rhotol

    # Dummy values to initialize vars, silence linter warnings
    rho_prev, omega, alpha, p, v = None, None, None, None, None

    r = b - matvec(x) if x.any() else b.copy()
    rtilde = r.copy()

    for iteration in range(maxiter):
        if np.linalg.norm(r) < atol:  # Are we done?
            return x, 0

        rho = dotprod(rtilde, r)
        if np.abs(rho) < rhotol:  # rho breakdown
            return x, -10

        if iteration > 0:
            if np.abs(omega) < omegatol:  # omega breakdown
                return x, -11

            beta = (rho / rho_prev) * (alpha / omega)
            p -= omega*v
            p *= beta
            p += r
        else:  # First spin
            s = np.empty_like(r)
            p = r.copy()

        phat = psolve(p)
        v = matvec(phat)
        rv = dotprod(rtilde, v)
        if rv == 0:
            return x, -11
        alpha = rho / rv
        r -= alpha*v
        s[:] = r[:]

        if np.linalg.norm(s) < atol:
            x += alpha*phat
            return x, 0

        shat = psolve(s)
        t = matvec(shat)
        omega = dotprod(t, s) / dotprod(t, t)
        x += alpha*phat
        x += omega*shat
        r -= omega*t
        rho_prev = rho

        if callback:
            callback(x)

    else:  # for loop exhausted
        # Return incomplete progress
        return x, maxiter


def bicgstab(A, b, x0=None, *, tol=1e-5, atol=0.0, maxiter=None, M=None):
  """Use Bi-Conjugate Gradient Stable iteration to solve ``Ax = b``.

  The numerics of JAX's ``bicgstab`` should exact match SciPy's
  ``bicgstab`` (up to numerical precision), but note that the interface
  is slightly different: you need to supply the linear operator ``A`` as
  a function instead of a sparse matrix or ``LinearOperator``.

  As with ``cg``, derivatives of ``bicgstab`` are implemented via implicit
  differentiation with another ``bicgstab`` solve, rather than by
  differentiating *through* the solver. They will be accurate only if
  both solves converge.

  Parameters
  ----------
  A: ndarray, function, or matmul-compatible object
      2D array or function that calculates the linear map (matrix-vector
      product) ``Ax`` when called like ``A(x)`` or ``A @ x``. ``A`` can represent
      any general (nonsymmetric) linear operator, and function must return array(s)
      with the same structure and shape as its argument.
  b : array or tree of arrays
      Right hand side of the linear system representing a single vector. Can be
      stored as an array or Python container of array(s) with any shape.

  Returns
  -------
  x : array or tree of arrays
      The converged solution. Has the same structure as ``b``.
  info : None
      Placeholder for convergence information. In the future, JAX will report
      the number of iterations when convergence is not achieved, like SciPy.

  Other Parameters
  ----------------
  x0 : array or tree of arrays
      Starting guess for the solution. Must have the same structure as ``b``.
  tol, atol : float, optional
      Tolerances for convergence, ``norm(residual) <= max(tol*norm(b), atol)``.
      We do not implement SciPy's "legacy" behavior, so JAX's tolerance will
      differ from SciPy unless you explicitly pass ``atol`` to SciPy's ``cg``.
  maxiter : integer
      Maximum number of iterations.  Iteration will stop after maxiter
      steps even if the specified tolerance has not been achieved.
  M : ndarray, function, or matmul-compatible object
      Preconditioner for A.  The preconditioner should approximate the
      inverse of A.  Effective preconditioning dramatically improves the
      rate of convergence, which implies that fewer iterations are needed
      to reach a given error tolerance.

  See also
  --------
  scipy.sparse.linalg.bicgstab
  jax.lax.custom_linear_solve
  """

  return _isolve(_bicgstab_solve,
                 A=A, b=b, x0=x0, tol=tol, atol=atol,
                 maxiter=maxiter, M=M)

