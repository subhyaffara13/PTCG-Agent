
def scale_by_loss():
  """Scale the gradient by the absolute value of the loss."""

  def update_fn(updates, state, params, *, loss, **extra_args):
    del params, extra_args
    updates = jax.tree.map(lambda u: u / loss, updates)
    return updates, state

  return base.GradientTransformationExtraArgs(base.init_empty_state, update_fn)


def scale_by_loss():
  """Scale the gradient by the absolute value of the loss."""

  def init_fn(params):
    del params
    return base.EmptyState()

  def update_fn(updates, state, params, *, loss, **extra_args):
    del params, extra_args
    updates = jax.tree.map(lambda u: u / loss, updates)
    return updates, state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

