
def incremental_update(
    new_tensors: base.Params, old_tensors: base.Params,
    step_size: jax.typing.ArrayLike) -> base.Params:
  """Incrementally update parameters via polyak averaging.

  Polyak averaging tracks an (exponential moving) average of the past
  parameters of a model, for use at test/evaluation time.

  Args:
    new_tensors: the latest value of the tensors.
    old_tensors: a moving average of the values of the tensors.
    step_size: the step_size used to update the polyak average on each step.

  Returns:
    an updated moving average `step_size*new+(1-step_size)*old` of the params.

  References:
    [Polyak et al, 1991](https://epubs.siam.org/doi/10.1137/0330046)
  """
  return jax.tree.map(
      lambda new, old: (
          None if new is None else step_size * new + (1.0 - step_size) * old
      ),
      new_tensors,
      old_tensors,
      is_leaf=lambda x: x is None,
  )

