
def warmup_cosine_decay_schedule(
    init_value: jax.typing.ArrayLike,
    peak_value: jax.typing.ArrayLike,
    warmup_steps: int,
    decay_steps: int,
    end_value: jax.typing.ArrayLike = 0.0,
    exponent: jax.typing.ArrayLike = 1.0,
) -> base.Schedule:
  r"""Linear warmup followed by cosine decay.

  Args:
    init_value: Initial value for the scalar to be annealed.
    peak_value: Peak value for scalar to be annealed at end of warmup.
    warmup_steps: Positive integer, the length of the linear warmup.
    decay_steps: Positive integer, the total length of the schedule. Note that
      this includes the warmup time, so the number of steps during which cosine
      annealing is applied is ``decay_steps - warmup_steps``.
    end_value: End value of the scalar to be annealed.
    exponent: The default decay is ``0.5 * (1 + cos(pi t/T))``, where ``t`` is
      the current timestep and ``T`` is ``decay_steps``. The exponent modifies
      this to be ``(0.5 * (1 + cos(pi * t/T))) ** exponent``. Defaults to 1.0.

  Returns:
    schedule
      A function that maps step counts to values
  """
  alpha = 0.0 if peak_value == 0.0 else end_value / peak_value
  schedules = [
      linear_schedule(
          init_value=init_value,
          end_value=peak_value,
          transition_steps=warmup_steps,
      ),
      cosine_decay_schedule(
          init_value=peak_value,
          decay_steps=decay_steps - warmup_steps,
          alpha=alpha,
          exponent=exponent,
      ),
  ]
  return _join.join_schedules(schedules, [warmup_steps])

