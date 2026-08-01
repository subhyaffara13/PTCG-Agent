
def scale_by_yogi(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-3,
    eps_root: jax.typing.ArrayLike = 0.0,
    initial_accumulator_value: jax.typing.ArrayLike = 1e-6,
) -> base.GradientTransformation:
  """Rescale updates according to the Yogi algorithm.

  See :func:`optax.yogi` for more details.

  Supports complex numbers, see
  https://gist.github.com/wdphy16/118aef6fb5f82c49790d7678cf87da29

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of variance of grads.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.
    initial_accumulator_value: The starting value for accumulators. Only
      positive values are allowed.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    # First moment
    mu = optax.tree.full_like(params, initial_accumulator_value)
    # Second moment
    nu = optax.tree.full_like(params, initial_accumulator_value)
    return ScaleByAdamState(count=jnp.zeros([], jnp.int32), mu=mu, nu=nu)

  def update_fn(updates, state, params=None):
    del params
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    nu = jax.tree.map(
        lambda g, v: v - (1 - b2) * jnp.sign(v - abs_sq(g)) * abs_sq(g),
        updates,
        state.nu,
    )
    count_inc = numerics.safe_increment(state.count)
    mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    nu_hat = optax.tree.bias_correction(nu, b2, count_inc)
    updates = jax.tree.map(
        lambda m, v: None if m is None else m / (jnp.sqrt(v + eps_root) + eps),
        mu_hat,
        nu_hat,
        is_leaf=lambda x: x is None,
    )
    return updates, ScaleByAdamState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

