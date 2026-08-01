
def cg(A, b, x0=None, *, rtol=1e-5, atol=0., maxiter=None, M=None, callback=None):
    """
    Solve ``Ax = b`` with the Conjugate Gradient method, for a symmetric,
    positive-definite `A`.

    Parameters
    ----------
    A : {sparse array, ndarray, LinearOperator}
        The real or complex N-by-N matrix of the linear system.
        `A` must represent a hermitian, positive definite matrix.
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
        Preconditioner for `A`. `M` must represent a hermitian, positive definite
        matrix. It should approximate the inverse of `A` (see Notes).
        Effective preconditioning dramatically improves the
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

    Notes
    -----
    The preconditioner `M` should be a matrix such that ``M @ A`` has a smaller
    condition number than `A`, see [2]_.

    References
    ----------
    .. [1] "Conjugate Gradient Method, Wikipedia, 
           https://en.wikipedia.org/wiki/Conjugate_gradient_method
    .. [2] "Preconditioner", 
           Wikipedia, https://en.wikipedia.org/wiki/Preconditioner

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import cg
    >>> P = np.array([[4, 0, 1, 0],
    ...               [0, 5, 0, 0],
    ...               [1, 0, 3, 2],
    ...               [0, 0, 2, 4]])
    >>> A = csc_array(P)
    >>> b = np.array([-1, -0.5, -1, 2])
    >>> x, exit_code = cg(A, b, atol=1e-5)
    >>> print(exit_code)    # 0 indicates successful convergence
    0
    >>> np.allclose(A.dot(x), b)
    True
    """
    A, M, x, b = make_system(A, M, x0, b)
    bnrm2 = np.linalg.norm(b)

    atol, _ = _get_atol_rtol('cg', bnrm2, atol, rtol)

    if bnrm2 == 0:
        return b, 0

    n = len(b)

    if maxiter is None:
        maxiter = n*10

    dotprod = np.vdot if np.iscomplexobj(x) else np.dot

    matvec = A.matvec
    psolve = M.matvec
    r = b - matvec(x) if x.any() else b.copy()

    # Dummy value to initialize var, silences warnings
    rho_prev, p = None, None

    for iteration in range(maxiter):
        if np.linalg.norm(r) < atol:  # Are we done?
            return x, 0

        z = psolve(r)
        rho_cur = dotprod(r, z)
        if iteration > 0:
            beta = rho_cur / rho_prev
            p *= beta
            p += z
        else:  # First spin
            p = np.empty_like(r)
            p[:] = z[:]

        q = matvec(p)
        alpha = rho_cur / dotprod(p, q)
        x += alpha*p
        r -= alpha*q
        rho_prev = rho_cur

        if callback:
            callback(x)

    else:  # for loop exhausted
        # Return incomplete progress
        return x, maxiter


def cg(A, b, x0=None, *, tol=1e-5, atol=0.0, maxiter=None, M=None):
  """Use Conjugate Gradient iteration to solve ``Ax = b``.

  The numerics of JAX's ``cg`` should exact match SciPy's ``cg`` (up to
  numerical precision), but note that the interface is slightly different: you
  need to supply the linear operator ``A`` as a function instead of a sparse
  matrix or ``LinearOperator``.

  Derivatives of ``cg`` are implemented via implicit differentiation with
  another ``cg`` solve, rather than by differentiating *through* the solver.
  They will be accurate only if both solves converge.

  Parameters
  ----------
  A: ndarray, function, or matmul-compatible object
      2D array or function that calculates the linear map (matrix-vector
      product) ``Ax`` when called like ``A(x)`` or ``A @ x``. ``A`` must represent
      a hermitian, positive definite matrix, and must return array(s) with the
      same structure and shape as its argument.
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
  scipy.sparse.linalg.cg
  jax.lax.custom_linear_solve
  """
  return _isolve(_cg_solve,
                 A=A, b=b, x0=x0, tol=tol, atol=atol,
                 maxiter=maxiter, M=M, check_symmetric=True)

