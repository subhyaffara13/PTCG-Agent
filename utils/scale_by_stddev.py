
def scale_by_stddev(
    decay: jax.typing.ArrayLike = 0.9,
    eps: jax.typing.ArrayLike = 1e-8,
    initial_scale: jax.typing.ArrayLike = 0.0,
    eps_in_sqrt: bool = True,
    bias_correction: bool = False,
) -> base.GradientTransformation:
  """Rescale updates by the root of the centered exp. moving average of squares.

  See :func:`optax.rmsprop` for more details.

  Args:
    decay: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.
    initial_scale: Initial value for second moment.
    eps_in_sqrt: Whether to add ``eps`` in the square root of the denominator or
      outside the square root.
    bias_correction: Whether to apply bias correction to the first and second
      moment.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    mu = optax.tree.zeros_like(params)  # First moment
    nu = optax.tree.full_like(params, initial_scale)  # second moment
    if bias_correction:
      return ScaleByRStdDevWithCountState(
          count=jnp.zeros([], jnp.int32), mu=mu, nu=nu
      )
    return ScaleByRStdDevState(mu=mu, nu=nu)

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, decay, 1)
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, decay, 2)
    if bias_correction:
      count_inc = numerics.safe_increment(state.count)
      mu_hat = optax.tree.bias_correction(mu, decay, count_inc)
      nu_hat = optax.tree.bias_correction(nu, decay, count_inc)
    else:
      count_inc = jnp.asarray(0)
      mu_hat = mu
      nu_hat = nu

    if eps_in_sqrt:
      scaling = jax.tree.map(
          lambda m, n: jax.lax.rsqrt(n - abs_sq(m) + eps),
          mu_hat,
          nu_hat,
      )
    else:
      scaling = jax.tree.map(
          lambda m, n: 1 / (jnp.sqrt(n - abs_sq(m)) + eps),
          mu_hat,
          nu_hat,
      )
    updates = jax.tree.map(lambda s, g: s * g, scaling, updates)
    if bias_correction:
      new_state = ScaleByRStdDevWithCountState(count=count_inc, mu=mu, nu=nu)
    else:
      new_state = ScaleByRStdDevState(mu=mu, nu=nu)
    return updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

