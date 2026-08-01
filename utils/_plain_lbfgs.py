
def _plain_lbfgs(
    fun: Callable[[jnp.ndarray], jnp.ndarray],
    init_params: jnp.ndarray,
    stepsize: float = 1e-3,
    maxiter: int = 500,
    tol: float = 1e-3,
    memory_size: int = 10,
    scale_init_precond: bool = True,
) -> jnp.ndarray:
  """Plain implementation of LBFGS."""
  # Algorithm 7.5 in "Numerical Optimization" by Nocedal and Wright, 1999
  # Notations differ from reference above with the following correspondences
  # dws -> s, dus -> y, identity_scale -> gamma
  value_and_grad_fun = jax.value_and_grad(fun)

  w = init_params
  _, g = value_and_grad_fun(init_params)
  dws = []
  dus = []

  for it in range(maxiter):
    if scale_init_precond:
      if it == 0:
        identity_scale = jnp.minimum(1.0, 1.0 / jnp.sqrt(jnp.sum(g**2)))
      else:
        identity_scale = jnp.vdot(dus[-1], dws[-1])
        identity_scale /= jnp.sum(dus[-1] ** 2)
    else:
      identity_scale = 1.0

    direction = -_plain_preconditioning(dws, dus, g, identity_scale)
    w_old, g_old = w, g
    w = w + stepsize * direction
    _, g = value_and_grad_fun(w)

    dws.append(w - w_old)
    dus.append(g - g_old)

    if len(dws) > memory_size:
      dws = dws[1:]  # Pop left.
      dus = dus[1:]

    grad_norm = jnp.sqrt(jnp.sum(g**2))

    if grad_norm <= tol:
      break

  return w

