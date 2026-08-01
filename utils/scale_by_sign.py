
def scale_by_sign() -> base.GradientTransformation:
  """Compute the signs of the gradient elements.

  Returns:
    An optax.GradientTransformation that contains the signs of the input
    gradient.
  """

  def update_fn(updates, state, params=None):
    del params
    updates = jax.tree.map(jnp.sign, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

