
def join_schedules(
    schedules: Sequence[base.Schedule], boundaries: Sequence[int]
) -> base.Schedule:
  """Sequentially apply multiple schedules.

  Args:
    schedules: A list of callables (expected to be optax schedules). Each
      schedule will receive a step count indicating the number of steps since
      the previous boundary transition.
    boundaries: A list of integers (of length one less than schedules) that
      indicate when to transition between schedules.

  Returns:
    schedule: A function that maps step counts to values.
  """

  def schedule(step: jax.typing.ArrayLike) -> jax.typing.ArrayLike:
    output = schedules[0](step)
    for boundary, schedule in zip(boundaries, schedules[1:]):
      output = jnp.where(step < boundary, output, schedule(step - boundary))
    return output

  return schedule

