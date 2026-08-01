
def _bicgstab_solve(A, b, x0=None, *, maxiter, tol=1e-5, atol=0.0, M=_identity):

  # tolerance handling uses the "non-legacy" behavior of scipy.sparse.linalg.bicgstab
  bs = _vdot_real_tree(b, b)
  atol2 = jnp.maximum(jnp.square(tol) * bs, jnp.square(atol))

  # https://en.wikipedia.org/wiki/Biconjugate_gradient_stabilized_method#Preconditioned_BiCGSTAB

  def cond_fun(value):
    x, r, *_, k = value
    rs = _vdot_real_tree(r, r)
    # the last condition checks breakdown
    return (rs > atol2) & (k < maxiter) & (k >= 0)

  def body_fun(value):
    x, r, rhat, alpha, omega, rho, p, q, k = value
    rho_ = _vdot_tree(rhat, r)
    beta = rho_ / rho * alpha / omega
    p_ = _add(r, _mul(beta, _sub(p, _mul(omega, q))))
    phat = M(p_)
    q_ = A(phat)
    alpha_ = rho_ / _vdot_tree(rhat, q_)
    s = _sub(r, _mul(alpha_, q_))
    exit_early = _vdot_real_tree(s, s) < atol2
    shat = M(s)
    t = A(shat)
    omega_ = _vdot_tree(t, s) / _vdot_tree(t, t)  # make cases?
    x_ = tree_map(partial(jnp.where, exit_early),
                  _add(x, _mul(alpha_, phat)),
                  _add(x, _add(_mul(alpha_, phat), _mul(omega_, shat)))
                  )
    r_ = tree_map(partial(jnp.where, exit_early),
                  s, _sub(s, _mul(omega_, t)))
    k_ = jnp.where((omega_ == 0) | (alpha_ == 0), -11, k + 1)
    k_ = jnp.where((rho_ == 0), -10, k_)
    return x_, r_, rhat, alpha_, omega_, rho_, p_, q_, k_

  r0 = _sub(b, A(x0))
  rho0 = alpha0 = omega0 = lax_internal._convert_element_type(
      1, *dtypes.lattice_result_type(*tree_leaves(b)))
  initial_value = (x0, r0, r0, alpha0, omega0, rho0, r0, r0, 0)

  x_final, *_ = lax.while_loop(cond_fun, body_fun, initial_value)

  return x_final

