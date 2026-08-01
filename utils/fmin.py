
def fmin(self: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    return torch.where(torch.isnan(other) | (other > self), self, other)


def fmin(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.fmin(a, b)


def fmin(func, x0, args=(), xtol=1e-4, ftol=1e-4, maxiter=None, maxfun=None,
         full_output=0, disp=1, retall=0, callback=None, initial_simplex=None):
    """
    Minimize a function using the downhill simplex algorithm.

    This algorithm only uses function values, not derivatives or second
    derivatives.

    Parameters
    ----------
    func : callable func(x,*args)
        The objective function to be minimized.
    x0 : ndarray
        Initial guess.
    args : tuple, optional
        Extra arguments passed to func, i.e., ``f(x,*args)``.
    xtol : float, optional
        Absolute error in xopt between iterations that is acceptable for
        convergence.
    ftol : number, optional
        Absolute error in func(xopt) between iterations that is acceptable for
        convergence.
    maxiter : int, optional
        Maximum number of iterations to perform.
    maxfun : number, optional
        Maximum number of function evaluations to make.
    full_output : bool, optional
        Set to True if fopt and warnflag outputs are desired.
    disp : bool, optional
        Set to True to print convergence messages.
    retall : bool, optional
        Set to True to return list of solutions at each iteration.
    callback : callable, optional
        Called after each iteration, as callback(xk), where xk is the
        current parameter vector.
    initial_simplex : array_like of shape (N + 1, N), optional
        Initial simplex. If given, overrides `x0`.
        ``initial_simplex[j,:]`` should contain the coordinates of
        the jth vertex of the ``N+1`` vertices in the simplex, where
        ``N`` is the dimension.

    Returns
    -------
    xopt : ndarray
        Parameter that minimizes function.
    fopt : float
        Value of function at minimum: ``fopt = func(xopt)``.
    iter : int
        Number of iterations performed.
    funcalls : int
        Number of function calls made.
    warnflag : int
        1 : Maximum number of function evaluations made.
        2 : Maximum number of iterations reached.
    allvecs : list
        Solution at each iteration.

    See Also
    --------
    minimize: Interface to minimization algorithms for multivariate
        functions. See the 'Nelder-Mead' `method` in particular.

    Notes
    -----
    Uses a Nelder-Mead simplex algorithm to find the minimum of function of
    one or more variables.

    This algorithm has a long history of successful use in applications.
    But it will usually be slower than an algorithm that uses first or
    second derivative information. In practice, it can have poor
    performance in high-dimensional problems and is not robust to
    minimizing complicated functions. Additionally, there currently is no
    complete theory describing when the algorithm will successfully
    converge to the minimum, or how fast it will if it does. Both the ftol and
    xtol criteria must be met for convergence.

    References
    ----------
    .. [1] Nelder, J.A. and Mead, R. (1965), "A simplex method for function
           minimization", The Computer Journal, 7, pp. 308-313

    .. [2] Wright, M.H. (1996), "Direct Search Methods: Once Scorned, Now
           Respectable", in Numerical Analysis 1995, Proceedings of the
           1995 Dundee Biennial Conference in Numerical Analysis, D.F.
           Griffiths and G.A. Watson (Eds.), Addison Wesley Longman,
           Harlow, UK, pp. 191-208.

    Examples
    --------
    >>> def f(x):
    ...     return x**2

    >>> from scipy import optimize

    >>> minimum = optimize.fmin(f, 1)
    Optimization terminated successfully.
             Current function value: 0.000000
             Iterations: 17
             Function evaluations: 34
    >>> minimum[0]
    -8.8817841970012523e-16
    """
    opts = {'xatol': xtol,
            'fatol': ftol,
            'maxiter': maxiter,
            'maxfev': maxfun,
            'disp': disp,
            'return_all': retall,
            'initial_simplex': initial_simplex}

    callback = _wrap_callback(callback)
    res = _minimize_neldermead(func, x0, args, callback=callback, **opts)
    if full_output:
        retlist = res['x'], res['fun'], res['nit'], res['nfev'], res['status']
        if retall:
            retlist += (res['allvecs'], )
        return retlist
    else:
        if retall:
            return res['x'], res['allvecs']
        else:
            return res['x']


def fmin(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Return element-wise minimum of the input arrays.

  JAX implementation of :func:`numpy.fmin`.

  Args:
    x1: input array or scalar.
    x2: input array or scalar. x1 and x2 must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing the element-wise minimum of x1 and x2.

  Note:
    For each pair of elements, ``jnp.fmin`` returns:
      - the smaller of the two if both elements are finite numbers.
      - finite number if one element is ``nan``.
      - ``-inf`` if one element is ``-inf`` and the other is finite or ``nan``.
      - ``inf`` if one element is ``inf`` and the other is ``nan``.
      - ``nan`` if both elements are ``nan``.

  Examples:
    >>> jnp.fmin(2, 3)
    Array(2, dtype=int32, weak_type=True)
    >>> jnp.fmin(2, jnp.array([1, 4, 2, -1]))
    Array([ 1,  2,  2, -1], dtype=int32)

    >>> x1 = jnp.array([1, 3, 2])
    >>> x2 = jnp.array([2, 1, 4])
    >>> jnp.fmin(x1, x2)
    Array([1, 1, 2], dtype=int32)

    >>> x3 = jnp.array([1, 5, 3])
    >>> x4 = jnp.array([[2, 3, 1],
    ...                 [5, 6, 7]])
    >>> jnp.fmin(x3, x4)
    Array([[1, 3, 1],
           [1, 5, 3]], dtype=int32)

    >>> nan = jnp.nan
    >>> x5 = jnp.array([jnp.inf, 5, nan])
    >>> x6 = jnp.array([[2, 3, nan],
    ...                 [nan, 6, 7]])
    >>> jnp.fmin(x5, x6)
    Array([[ 2.,  3., nan],
           [inf,  5.,  7.]], dtype=float32)
  """
  # TODO(jakevdp) remove cast when jit type annotations improve
  mask = cast(Array, ufuncs.less(x1, x2) | ufuncs.isnan(x2))
  return where(mask, x1, x2)

