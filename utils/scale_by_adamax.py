
def scale_by_adamax(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8
) -> base.GradientTransformation:
  """Rescale updates according to the Adamax algorithm.

  See :func:`optax.adamax` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted maximum of grads.
    eps: Term added to the denominator to improve numerical stability.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    mu = optax.tree.zeros_like(params)  # First moment
    nu = optax.tree.zeros_like(params)  # Infinite moment
    return ScaleByAdamState(count=jnp.zeros([], jnp.int32), mu=mu, nu=nu)

  def update_fn(updates, state, params=None):
    del params
    count_inc = numerics.safe_increment(state.count)
    mu = optax.tree.update_moment(updates, state.mu, b1, 1)
    nu = optax.tree.update_infinity_moment(updates, state.nu, b2, eps)
    # Bias correction for mean. No bias correction needed for infinity moment.
    mu_hat = optax.tree.bias_correction(mu, b1, count_inc)
    updates = jax.tree.map(lambda m, v: m / v, mu_hat, nu)
    return updates, ScaleByAdamState(count=count_inc, mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

