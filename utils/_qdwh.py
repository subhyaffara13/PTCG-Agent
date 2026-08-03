import functools

def _qdwh(x, m, n, max_iterations, eps):
  """QR-based dynamically weighted Halley iteration for polar decomposition."""

  # Estimates `alpha` and `beta = alpha * l`, where `alpha` is an estimate of
  # norm(x, 2) such that `alpha >= norm(x, 2)` and `beta` is a lower bound for
  # the smallest singular value of x.
  if eps is None:
    eps = float(dtypes.finfo(x.dtype).eps)
  one_norm = jnp_linalg.norm(x, ord=1)
  inf_norm = jnp_linalg.norm(x, ord=np.inf)
  alpha_inverse = lax.rsqrt(one_norm) * lax.rsqrt(inf_norm)
  alpha_inverse = jnp.where(one_norm == 0, 1, alpha_inverse)
  u = x * alpha_inverse.astype(x.dtype)

  l = eps

  # Iteration tolerances.
  tol_l = 10.0 * eps / 2.0
  tol_norm = jnp.cbrt(tol_l)

  def get_qr_params(a, b, c):
    e = b / c
    a_minus_e = a - e
    sqrt_c = c ** (1 / 2)
    return (a_minus_e / sqrt_c, sqrt_c, e)

  def get_chol_params(a, b, c):
    e = b / c
    a_minus_e = a - e
    return (a_minus_e, c, e)

  CHOLESKY_CUTOFF = 100

  qr_coefs = []
  chol_coefs = []
  k = 0
  while l + tol_l < 1 and k < max_iterations:
    k += 1
    l2 = l * l
    dd = (4 * (1 / l2 - 1) / l2) ** (1 / 3)
    sqd = (1.0 + dd) ** (1 / 2)
    a = sqd + (2 - dd + 2 * (2 - l2) / (l2 * sqd)) ** (1 / 2)
    b = (a - 1) ** 2 / 4
    c = a + b - 1
    l = l * (a + b * l2) / (1 + c * l2)
    if c > CHOLESKY_CUTOFF:
      qr_coefs.append(get_qr_params(a, b, c))
    else:
      chol_coefs.append(get_chol_params(a, b, c))

  def iteration(k, state, update_fn, coefs, test_convergence):
    u, _ = state

    if coefs is None:
      # As l → 1, the coefficients a, b, c → 3, 1, 3, which is Halley's method.
      params = get_chol_params(3, 1, 3)
    else:
      params = lax.dynamic_index_in_dim(coefs, k, keepdims=False)

    u_prev = u
    u = update_fn(u, m, n, params)

    is_not_converged = True
    if test_convergence:
      is_not_converged = jnp_linalg.norm(u - u_prev) > tol_norm
    return u, is_not_converged

  def iterate(u, coefs, **kwargs):
    if not coefs:
      return u, True
    coefs = jnp.array(coefs).astype(x.dtype)
    body = functools.partial(iteration, coefs=coefs, **kwargs)
    return lax.fori_loop(0, len(coefs), body, (u, True))

  u, _ = iterate(
      u, coefs=qr_coefs, update_fn=_use_qr, test_convergence=False
  )
  u, is_not_converged = iterate(
      u, coefs=chol_coefs, update_fn=_use_cholesky, test_convergence=True
  )

  # If l has converged but u still has not, continue with Halley's method
  # (coef = None) until convergence.
  def cond_fun(state):
    k, _, is_not_converged = state
    return jnp.logical_and(is_not_converged, k < max_iterations)

  def body_fun(state):
    k, u, is_not_converged = state
    u, is_not_converged = iteration(
        k,
        (u, is_not_converged),
        coefs=None,
        update_fn=_use_cholesky,
        test_convergence=True,
    )
    return k + 1, u, is_not_converged

  k = len(qr_coefs) + len(chol_coefs)
  num_iters, u, is_not_converged = lax.while_loop(
      cond_fun, body_fun, (k, u, is_not_converged)
  )

  # Applies Newton-Schulz refinement for better accuracy.
  u = 1.5 * u - 0.5 * u @ (u.T.conj() @ u)

  h = u.T.conj() @ x
  h = (h + h.T.conj()) / 2

  # Converged within the maximum number of iterations.
  is_converged = jnp.logical_not(is_not_converged)

  return u, h, num_iters, is_converged

