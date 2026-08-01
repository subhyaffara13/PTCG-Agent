
def scale_by_novograd(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.25,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    weight_decay: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.GradientTransformation:
  """Computes NovoGrad updates.

  See :func:`optax.novograd` for more details.

  Args:
    b1: A decay rate for the exponentially weighted average of grads.
    b2: A decay rate for the exponentially weighted average of squared grads.
    eps: A term added to the denominator to improve numerical stability.
    eps_root: A term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.
    weight_decay: A scalar weight decay rate.
    mu_dtype: An optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.
  """

  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params):
    mu = optax.tree.zeros_like(params, dtype=mu_dtype)
    nu = jax.tree.map(lambda p: jnp.asarray(0.0, dtype=p.dtype), params)
    return ScaleByNovogradState(count=jnp.zeros([], jnp.int32), mu=mu, nu=nu)

  def nu_addition(grads):
    return jnp.linalg.norm(grads) ** 2

  def mu_addition(grads, params, nu):
    return grads / (jnp.sqrt(nu + eps_root) + eps) + weight_decay * params

  def init_nu(grads, nu):
    return jax.tree.map(lambda g, n: nu_addition(g).astype(n.dtype), grads, nu)

  def update_nu(grads, nu):
    updates = jax.tree.map(nu_addition, grads)
    return optax.tree.update_moment(updates, nu, b2, 1)

  def init_mu(grads, params, mu, nu):
    del mu
    return jax.tree.map(mu_addition, grads, params, nu)

  def update_mu(grads, params, mu, nu):
    updates = jax.tree.map(mu_addition, grads, params, nu)
    return jax.tree.map(
        lambda m, u: None if m is None else b1 * m + u,
        mu,
        updates,
        is_leaf=lambda x: x is None,
    )

  def update_fn(updates, state, params):
    count_inc = numerics.safe_increment(state.count)

    nu = jax.lax.cond(count_inc == 1, init_nu, update_nu, updates, state.nu)
    mu = jax.lax.cond(
        count_inc == 1, init_mu, update_mu, updates, params, state.mu, nu
    )

    mu = optax.tree.cast(mu, mu_dtype)
    updates = mu
    return updates, ScaleByNovogradState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

