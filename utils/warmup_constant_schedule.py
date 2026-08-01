
def warmup_constant_schedule(
    init_value: jax.typing.ArrayLike,
    peak_value: jax.typing.ArrayLike,
    warmup_steps: int,
) -> base.Schedule:
  r"""Linear warmup followed by constant schedule i.e no decay.

  Args:
    init_value: Initial value for the scalar to be annealed.
    peak_value: Peak value for scalar to be annealed at end of warmup.
    warmup_steps: Positive integer, the length of the linear warmup.

  Returns:
    schedule
      A function that maps step counts to values
  """
  return linear_schedule(
      init_value=init_value,
      end_value=peak_value,
      transition_steps=warmup_steps,
  )

