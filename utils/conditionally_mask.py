
def conditionally_mask(
    inner: base.GradientTransformation,
    should_transform_fn: ConditionFn,
    forward_extra_args: bool = False,
) -> base.GradientTransformationExtraArgs:
  """Calls the inner update function only at certain steps.

  Creates a transformation wrapper that conditionally applies the inner gradient
  transformation, and if the condition is not met, the updates are set to 0,
  while the inner state is passed through unchanged. The behavior is controlled
  by a user specified function ``should_transform_fn`` that is called
  by ``conditionally_transform`` passing as input a counter of the number of
  times that the ``update`` function has been previously called, the user
  specified function must returns a boolean controlling whether the inner
  transformation should be called.

  Args:
    inner: the inner transformation.
    should_transform_fn: function takes in a step counter (array of shape [] and
      dtype ``int32``), and returns a boolean array of shape []. If
      ``forward_extra_args`` is set to True, any extra arguments are also
      forwarded to the ``should_transform_fn``.
    forward_extra_args: forward extra args to ``should_transform_fn``.

  Returns:
    A new :class:`optax.GradientTransformationExtraArgs`.

  .. warning::
    If instead you want to leave ``updates`` unchanged when the condition
    is not met, you can use the ``conditionally_transform`` wrapper.

  .. versionadded:: 0.2.3
  """
  inner = base.with_extra_args_support(inner)

  def init_fn(params):
    return ConditionallyMaskState(
        step=jnp.zeros([], jnp.int32), inner_state=inner.init(params)
    )

  def update_fn(updates, state, params=None, **extra_args):

    def do_update(_):
      return inner.update(updates, state.inner_state, params, **extra_args)

    def reject_update(_):
      return optax.tree.zeros_like(updates), state.inner_state

    condition_kwargs = extra_args if forward_extra_args else {}
    updates, new_inner_state = lax.cond(
        should_transform_fn(state.step, **condition_kwargs),
        do_update,
        reject_update,
        operand=None,
    )

    return updates, ConditionallyMaskState(
        step=numerics.safe_increment(state.step),
        inner_state=new_inner_state,
    )

  return base.GradientTransformationExtraArgs(init_fn, update_fn)

