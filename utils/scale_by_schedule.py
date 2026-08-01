
def scale_by_schedule(
    step_size_fn: base.Schedule,
) -> base.GradientTransformation:
  """Scale updates using a custom schedule for the `step_size`.

  Args:
    step_size_fn: A function that takes an update count as input and proposes
      the step_size to multiply the updates by.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    del params
    return ScaleByScheduleState(count=jnp.zeros([], jnp.int32))

  def update_fn(updates, state, params=None):
    del params
    step_size = step_size_fn(state.count)
    updates = jax.tree.map(
        lambda g: jnp.array(step_size, dtype=g.dtype) * g, updates
    )
    return updates, ScaleByScheduleState(
        count=numerics.safe_increment(state.count)
    )

  return base.GradientTransformation(init_fn, update_fn)

