
def keep_params_nonnegative() -> base.GradientTransformation:
  """Modifies the updates to keep parameters non-negative, i.e. >= 0.

  This transformation ensures that parameters after the update will be
  larger than or equal to zero.
  In a chain of transformations, this should be the last one.

  Returns:
    A :class:`optax.GradientTransformation` object.

  .. warning::
    The transformation expects input params to be non-negative.
    When params is negative the transformed update will move them to 0.
  """

  def init_fn(params):
    del params
    return NonNegativeParamsState()

  def update_fn(updates, state, params):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)

    updates = jax.tree.map(
        lambda p, u: None if p is None else jnp.where((p + u) < 0.0, -p, u),
        params,
        updates,
        is_leaf=lambda x: x is None,
    )
    return updates, state

  return base.GradientTransformation(init_fn, update_fn)

