
def track_per_element_mean_and_variance_with_ema(
    ema_decay: jax.typing.ArrayLike = 0.9,
) -> base.GradientTransformation:
  """Track variance metrics with an EMA over time.

  See :func:`optax.experimental.aggregating.add_mean_variance_to_opt` for a
  complete example.

  Args:
    ema_decay: The EMA decay factor.

  Returns:
    A GradientTransformation that tracks per-element mean and variance with an
    EMA over time. The mean and variance are computed thanks to the auxiliary
    arguments provided by the `get_per_element_mean_and_sum_sq_diff_grads`
    aggregator when this transformation is linked with it via
    :func:`optax.experimental.aggregating.process`.
  """

  def init_fn(params):
    return PerElementMeanAndVarianceEMAState(
        count=jnp.zeros([], jnp.int32),
        ema_decay=jnp.asarray(ema_decay),
        mean_grads_ema=tree.zeros_like(params),
        variance_grads_ema=tree.zeros_like(params),
    )

  def update_fn(updates, state, params=None, *, sum_sq_diff_grads, sample_size):
    del params
    mean_grads_ema = jax.tree.map(
        lambda x, y: (1.0 - ema_decay) * x + ema_decay * y,
        updates,
        state.mean_grads_ema,
    )
    variance_step = tree.scale(1 / (sample_size - 1), sum_sq_diff_grads)
    variance_grads_ema = jax.tree.map(
        lambda x, y: (1.0 - ema_decay) * x + ema_decay * y,
        variance_step,
        state.variance_grads_ema,
    )
    new_count = utils.safe_int32_increment(state.count)
    new_state = state._replace(
        count=new_count,
        mean_grads_ema=mean_grads_ema,
        variance_grads_ema=variance_grads_ema,
    )
    return updates, new_state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

