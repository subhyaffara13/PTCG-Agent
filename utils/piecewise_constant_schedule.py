
def piecewise_constant_schedule(
    init_value: jax.typing.ArrayLike,  # float
    boundaries_and_scales: Optional[dict[int, float]] = None
) -> base.Schedule:
  """Piecewise constant schedule with scaled jumps at specific boundaries.

  At each step `t`, this schedule returns `init_value` scaled by the product
  of all factors `f_i` such that `t >= b_i`, where `(b_i, f_i)` are the
  entries in `boundaries_and_scales`.

  Args:
    init_value: The starting value of the schedule.
    boundaries_and_scales: Dictionary of `{step: scale}` where `scale` is
      multiplied into the schedule value at the given `step`. All `scale` values
      must be non-negative.

  Returns:
    A function that maps step index to schedule value.

  Example:
    >>> sched = optax.piecewise_constant_schedule(
    ...     init_value=1.0, boundaries_and_scales={100: 0.1, 200: 0.01})
    >>> print(sched(50))   # before first boundary
    1.0
    >>> print(sched(150))  # after first boundary
    0.1
    >>> print(sched(250))  # after second boundary
    0.001
  """
  if boundaries_and_scales is not None:
    all_positive = all(scale >= 0.0 for scale in boundaries_and_scales.values())
    if not all_positive:
      raise ValueError(
          '`piecewise_constant_schedule` expects non-negative scale factors'
      )

  def schedule(count):
    v = init_value
    if boundaries_and_scales is not None:
      for threshold, scale in sorted(boundaries_and_scales.items()):
        indicator = jnp.maximum(0.0, jnp.sign(threshold - count))
        v = v * indicator + (1 - indicator) * scale * v
    return v

  return schedule

