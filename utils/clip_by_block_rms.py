
def clip_by_block_rms(
    threshold: jax.typing.ArrayLike
) -> base.GradientTransformation:
  """Clips updates to a max rms for the gradient of each param vector or matrix.

  A `block` is here a weight vector (e.g. in a Linear layer) or a weight matrix
  (e.g. in a convolutional layer) appearing as a leaf in the grads/param pytree.

  Args:
    threshold: The maximum rms for the gradient of each param vector or matrix.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params

    def _clip_fn(u):
      clip_denom = jnp.maximum(
          1.0, jnp.sqrt(jnp.mean(numerics.abs_sq(u))) / threshold
      )
      return u / clip_denom

    updates = jax.tree.map(_clip_fn, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

