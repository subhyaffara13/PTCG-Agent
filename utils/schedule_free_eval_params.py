
def schedule_free_eval_params(state: base.OptState, params: base.Params):
  """Params for evaluation of :func:`optax.contrib.schedule_free`."""
  # Using ScheduleFreeState as a type hint above results in pytype errors in
  # tests.
  b1 = getattr(state, 'b1')
  z = getattr(state, 'z')
  if b1 is None or z is None:
    raise ValueError(
        'schedule_free_eval_params requires a ScheduleFreeState as input.'
    )
  return jax.tree.map(lambda yi, zi: (yi - (1.0 - b1) * zi) / b1, params, z)

