
def _minimize_lbfgs(
    fun: Callable,
    x0: Array,
    maxiter: float | None = None,
    norm=np.inf,
    maxcor: int = 10,
    ftol: float = 2.220446049250313e-09,
    gtol: float = 1e-05,
    maxfun: float | None = None,
    maxgrad: float | None = None,
    maxls: int = 20,
):
  """
  Minimize a function using L-BFGS

  Implements the L-BFGS algorithm from
    Algorithm 7.5 from Wright and Nocedal, 'Numerical Optimization', 1999, pg. 176-185
  And generalizes to complex variables from
     Sorber, L., Barel, M.V. and Lathauwer, L.D., 2012.
     "Unconstrained optimization of real functions in complex variables"
     SIAM Journal on Optimization, 22(3), pp.879-898.

  Args:
    fun: function of the form f(x) where x is a flat ndarray and returns a real scalar.
      The function should be composed of operations with vjp defined.
    x0: initial guess
    maxiter: maximum number of iterations
    norm: order of norm for convergence check. Default inf.
    maxcor: maximum number of metric corrections ("history size")
    ftol: terminates the minimization when `(f_k - f_{k+1}) < ftol`
    gtol: terminates the minimization when `|g_k|_norm < gtol`
    maxfun: maximum number of function evaluations
    maxgrad: maximum number of gradient evaluations
    maxls: maximum number of line search steps (per iteration)

  Returns:
    Optimization results.
  """
  d = len(x0)
  dtype = dtypes.dtype(x0)

  # ensure there is at least one termination condition
  if (maxiter is None) and (maxfun is None) and (maxgrad is None):
    maxiter = d * 200

  # set others to inf, such that >= is supported
  if maxiter is None:
    maxiter = np.inf
  if maxfun is None:
    maxfun = np.inf
  if maxgrad is None:
    maxgrad = np.inf

  # initial evaluation
  f_0, g_0 = api.value_and_grad(fun)(x0)
  state_initial = LBFGSResults(
    converged=jnp.array(False, dtype=bool),
    failed=jnp.array(False, dtype=bool),
    k=0,
    nfev=1,
    ngev=1,
    x_k=x0,
    f_k=f_0,
    g_k=g_0,
    s_history=jnp.zeros((maxcor, d), dtype=dtype),
    y_history=jnp.zeros((maxcor, d), dtype=dtype),
    rho_history=jnp.zeros((maxcor,), dtype=dtype),
    gamma=1.,
    status=0,
    ls_status=0,
  )

  def cond_fun(state: LBFGSResults):
    return (~state.converged) & (~state.failed)

  def body_fun(state: LBFGSResults):
    # find search direction
    p_k = _two_loop_recursion(state)

    # line search
    ls_results = line_search(
      f=fun,
      xk=state.x_k,
      pk=p_k,
      old_fval=state.f_k,
      gfk=state.g_k,
      maxiter=maxls,
    )

    # evaluate at next iterate
    s_k = jnp.asarray(ls_results.a_k).astype(p_k.dtype) * p_k
    x_kp1 = state.x_k + s_k
    f_kp1 = ls_results.f_k
    g_kp1 = ls_results.g_k
    y_k = g_kp1 - state.g_k
    rho_k_inv = jnp.real(_dot(y_k, s_k))
    rho_k = jnp.reciprocal(rho_k_inv).astype(y_k.dtype)
    gamma = rho_k_inv / jnp.real(_dot(jnp.conj(y_k), y_k))

    # replacements for next iteration
    status = jnp.array(0)
    status = jnp.where(state.f_k - f_kp1 < ftol, 4, status)
    status = jnp.where(state.ngev >= maxgrad, 3, status)
    status = jnp.where(state.nfev >= maxfun, 2, status)
    status = jnp.where(state.k >= maxiter, 1, status)
    status = jnp.where(ls_results.failed, 5, status)

    converged = jnp_linalg.norm(g_kp1, ord=norm) < gtol

    # TODO(jakevdp): use a fixed-point procedure rather than type-casting?
    state = state._replace(
      converged=converged,
      failed=(status > 0) & (~converged),
      k=state.k + 1,
      nfev=state.nfev + ls_results.nfev,
      ngev=state.ngev + ls_results.ngev,
      x_k=x_kp1.astype(state.x_k.dtype),
      f_k=f_kp1.astype(state.f_k.dtype),
      g_k=g_kp1.astype(state.g_k.dtype),
      s_history=_update_history_vectors(history=state.s_history, new=s_k),
      y_history=_update_history_vectors(history=state.y_history, new=y_k),
      rho_history=_update_history_scalars(history=state.rho_history, new=rho_k),
      gamma=gamma.astype(state.g_k.dtype),
      status=jnp.where(converged, 0, status),
      ls_status=ls_results.status,
    )

    return state

  return lax.while_loop(cond_fun, body_fun, state_initial)

