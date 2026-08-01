
def constant_schedule(value: jax.typing.ArrayLike) -> base.Schedule:
  """Constructs a constant schedule.

  Args:
    value: value to be held constant throughout.

  Returns:
    schedule
      A function that maps step counts to values.

  Examples:
    >>> schedule_fn = optax.constant_schedule(5)
    >>> schedule_fn(0)
    5
    >>> schedule_fn(100)
    5
  """
  return lambda count: value

