
def get_unbiased_mean_and_variance_ema(
    state: base.OptState,
) -> tuple[base.Updates, base.Updates]:
  """Retrieve unbiased mean and variance from the state.

  Args:
    state: The state of the optimizer.

  Returns:
    A tuple of unbiased mean and variance EMA.
  """
  per_elt_mean_and_variance_ema_state = tree.get(
      state, 'PerElementMeanAndVarianceEMAState', None
  )
  if per_elt_mean_and_variance_ema_state is None:
    raise ValueError(
        'State must have PerElementMeanAndVarianceEMAState to compute unbiased'
        ' mean and variance EMA.'
    )
  count = per_elt_mean_and_variance_ema_state.count
  ema_decay = per_elt_mean_and_variance_ema_state.ema_decay
  mean_grads_ema = per_elt_mean_and_variance_ema_state.mean_grads_ema
  variance_grads_ema = per_elt_mean_and_variance_ema_state.variance_grads_ema
  unbiased_mean_grads_ema = jax.tree.map(
      lambda x: x / (1 - ema_decay**count), mean_grads_ema
  )
  unbiased_variance_grads_ema = jax.tree.map(
      lambda x: x / (1 - ema_decay**count), variance_grads_ema
  )
  return unbiased_mean_grads_ema, unbiased_variance_grads_ema

