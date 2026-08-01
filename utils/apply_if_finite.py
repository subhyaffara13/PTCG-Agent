
def apply_if_finite(
    inner: base.GradientTransformation, max_consecutive_errors: int
) -> base.GradientTransformation:
  """A function that wraps an optimizer to make it robust to a few NaNs or Infs.

  The purpose of this function is to prevent any optimization to happen if the
  gradients contain NaNs or Infs. That is, when a NaN or Inf is detected in the
  gradients, the wrapped optimizer ignores that gradient update. If the NaNs or
  Infs persist after a given number of updates, the wrapped optimizer gives up
  and accepts the update.

  Args:
    inner: Inner transformation to be wrapped.
    max_consecutive_errors: Maximum number of consecutive gradient updates
      containing NaNs or Infs that the wrapped optimizer will ignore. After that
      many ignored updates, the optimizer will give up and accept.

  Returns:
    New :class:`optax.GradientTransformationExtraArgs`.
  """

  inner = base.with_extra_args_support(inner)

  def init(params):
    return ApplyIfFiniteState(
        notfinite_count=jnp.zeros([], jnp.int32),
        last_finite=jnp.array(True, jnp.bool_),
        total_notfinite=jnp.zeros([], jnp.int32),
        inner_state=inner.init(params),
    )

  def update(updates, state, params=None, **extra_args):
    inner_state = state.inner_state
    flat_updates = jax.tree.flatten(updates)[0]
    isfinite = jnp.all(
        jnp.array([jnp.all(jnp.isfinite(p)) for p in flat_updates])
    )
    notfinite_count = jnp.where(
        isfinite,
        jnp.zeros([], jnp.int32),
        numerics.safe_increment(state.notfinite_count),
    )

    def do_update(_):
      return inner.update(updates, inner_state, params, **extra_args)

    def reject_update(_):
      return optax.tree.zeros_like(updates), inner_state

    updates, new_inner_state = lax.cond(
        jnp.logical_or(isfinite, notfinite_count > max_consecutive_errors),
        do_update,
        reject_update,
        operand=None,
    )

    return updates, ApplyIfFiniteState(
        notfinite_count=notfinite_count,
        last_finite=isfinite,
        total_notfinite=jnp.where(
            isfinite,
            state.total_notfinite,
            numerics.safe_increment(state.total_notfinite),
        ),
        inner_state=new_inner_state,
    )

  return base.GradientTransformationExtraArgs(init=init, update=update)

