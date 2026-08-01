
def set_to_zero() -> GradientTransformation:
  """Stateless transformation that maps input gradients to zero.

  The resulting update function, when called, will return a tree of zeros
  matching the shape of the input gradients. This means that when the updates
  returned from this transformation are applied to the model parameters, the
  model parameters will remain unchanged.

  This can be used in combination with `partition` or `masked` to freeze
  (i.e. keep fixed) some parts of the tree of model parameters while applying
  gradient updates to other parts of the tree.

  When updates are set to zero inside the same jit-compiled function as the
  calculation of gradients, optax transformations, and application of updates to
  parameters, unnecessary computations will in general be dropped.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params  # Unused by the zero transform.
    return jax.tree.map(jnp.zeros_like, updates), state

  return GradientTransformation(init_empty_state, update_fn)

