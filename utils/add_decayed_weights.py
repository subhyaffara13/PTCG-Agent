
def add_decayed_weights(
    weight_decay: base.ScalarOrSchedule = 0.0,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
) -> base.GradientTransformation:
  """Add parameter scaled by `weight_decay`.

  Args:
    weight_decay: A scalar weight decay rate.
    mask: A tree with same structure as (or a prefix of) the params PyTree, or a
      Callable that returns such a pytree given the params/updates. The leaves
      should be booleans, `True` for leaves/subtrees you want to apply the
      transformation to, and `False` for those you want to skip.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    del params
    if callable(weight_decay):
      return WeightDecaySchedule(count=jnp.zeros([], jnp.int32))
    else:
      return base.EmptyState()

  def update_fn(updates, state, params):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)
    if callable(weight_decay):
      new_state = WeightDecaySchedule(numerics.safe_increment(state.count))
    else:
      new_state = state

    # If weight decay is a zero constant, we can skip the update.
    if isinstance(weight_decay, (int, float)) and weight_decay == 0.0:
      return updates, new_state

    s = weight_decay(state.count) if callable(weight_decay) else weight_decay
    updates = jax.tree.map(
        lambda g, p: None if g is None else g + s * p,
        updates,
        params,
        is_leaf=lambda x: x is None,
    )
    return updates, new_state

  # If mask is not `None`, apply mask to the gradient transformation.
  # E.g. it is common to skip weight decay on bias units and batch stats.
  if mask is not None:
    return wrappers.masked(
        base.GradientTransformation(init_fn, update_fn), mask
    )
  return base.GradientTransformation(init_fn, update_fn)

