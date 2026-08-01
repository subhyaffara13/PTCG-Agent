
def scale_by_rss(
    initial_accumulator_value: jax.typing.ArrayLike = 0.1,
    eps: jax.typing.ArrayLike = 1e-7
) -> base.GradientTransformation:
  """Rescale updates by the root of the sum of all squared gradients to date.

  See :func:`optax.adagrad` for more details.

  Args:
    initial_accumulator_value: Starting value for accumulators, must be >= 0.
    eps: A small floating point value to avoid zero denominator.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    return ScaleByRssState(
        sum_of_squares=optax.tree.full_like(params, initial_accumulator_value)
    )

  def update_fn(updates, state, params=None):
    del params
    sum_of_squares = jax.tree.map(
        lambda g, t: abs_sq(g) + t, updates, state.sum_of_squares
    )
    inv_sqrt_g_square = jax.tree.map(
        lambda t: jnp.where(t > 0, jax.lax.rsqrt(t + eps), 0.0), sum_of_squares
    )
    updates = optax.tree.mul(inv_sqrt_g_square, updates)
    return updates, ScaleByRssState(sum_of_squares=sum_of_squares)

  return base.GradientTransformation(init_fn, update_fn)

