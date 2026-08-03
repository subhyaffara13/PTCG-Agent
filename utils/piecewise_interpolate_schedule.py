from typing import Optional

def piecewise_interpolate_schedule(
    interpolate_type: str,
    init_value: jax.typing.ArrayLike,
    boundaries_and_scales: Optional[dict[int, float]] = None,
) -> base.Schedule:
  """Piecewise interpolated schedule with linear or cosine transitions.

  This schedule interpolates smoothly between values scaled at specified
  step boundaries. The interpolation occurs **between the accumulated scaled
  values**, not the raw multiplicative scales themselves.

  At each boundary, the scaling factor is multiplied into the current value.
  Between these boundaries, the schedule applies either linear or cosine
  interpolation.

  Args:
    interpolate_type: Either `'linear'` or `'cosine'`, specifying the
      interpolation method used between boundary segments.
    init_value: Starting value for the schedule.
    boundaries_and_scales: A dictionary `{step: scale}` that defines the
      boundaries and their corresponding multiplicative scaling factors.

  Returns:
    A function that maps step counts to interpolated values.

  Example:
    >>> sched = optax.piecewise_interpolate_schedule(
    ...     interpolate_type='linear',
    ...     init_value=1.0,
    ...     boundaries_and_scales={4: 0.1, 8: 0.01}
    ... )
    >>> for step in range(0, 11, 2):
    ...     print(f"Step {step}: {sched(step):.6f}")
    Step 0: 1.000000
    Step 2: 0.550000
    Step 4: 0.100000
    Step 6: 0.050500
    Step 8: 0.001000
    Step 10: 0.001000

    .. note::
      This schedule accumulates scaling factors and then interpolates between
      those accumulated values. It does *not* interpolate directly between the
      provided scales. This behavior can appear counterintuitive but allows
      for smooth and controlled transitions in learning rates.
  """

  if interpolate_type == 'linear':
    interpolate_fn = _linear_interpolate
  elif interpolate_type == 'cosine':
    interpolate_fn = _cosine_interpolate
  else:
    raise ValueError("`interpolate_type` must be either 'cosine' or 'linear'")

  if boundaries_and_scales:
    boundaries, scales = zip(*sorted(boundaries_and_scales.items()))
    if not all(scale >= 0.0 for scale in scales):
      raise ValueError(
          '`piecewise_interpolate_schedule` expects non-negative scale factors'
      )
  else:
    boundaries, scales = (), ()

  def schedule(count):
    bounds = jnp.stack((0,) + boundaries)
    values = jnp.cumprod(jnp.stack((init_value,) + scales))
    interval_sizes = jnp.maximum(bounds[1:] - bounds[:-1], 1)
    indicator = jnp.logical_and(bounds[:-1] <= count, count < bounds[1:])
    pct = (count - bounds[:-1]) / interval_sizes
    interp_vals = interpolate_fn(values[:-1], values[1:], pct)
    return indicator.dot(interp_vals) + (bounds[-1] <= count) * values[-1]

  return schedule

