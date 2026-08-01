
def scale_by_param_block_rms(
    min_scale: jax.typing.ArrayLike = 1e-3,
) -> base.GradientTransformation:
  """Scale updates by rms of the gradient for each param vector or matrix.

  A `block` is here a weight vector (e.g. in a Linear layer) or a weight matrix
  (e.g. in a convolutional layer) appearing as a leaf in the grads/param pytree.

  Args:
    min_scale: Minimum scaling factor.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)
    updates = jax.tree.map(
        lambda u, p: u * numerics.safe_root_mean_squares(p, min_scale),
        updates,
        params,
    )
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

