
def warmup_exponential_decay_schedule(
    init_value: jax.typing.ArrayLike,
    peak_value: jax.typing.ArrayLike,
    warmup_steps: int,
    transition_steps: int,
    decay_rate: jax.typing.ArrayLike,
    transition_begin: int = 0,
    staircase: bool = False,
    end_value: Optional[jax.typing.ArrayLike] = None,
) -> base.Schedule:
  """Linear warmup followed by exponential decay.

  Args:
    init_value: Initial value for the scalar to be annealed.
    peak_value: Peak value for scalar to be annealed at end of warmup.
    warmup_steps: Positive integer, the length of the linear warmup.
    transition_steps: must be positive.
      See :func:`optax.schedules.exponential_decay` for more details.
    decay_rate: must not be zero. The decay rate.
    transition_begin: must be positive. After how many steps to start annealing
      (before this many steps the scalar value is held fixed at ``peak_value``).
    staircase: if ``True``, decay the values at discrete intervals.
    end_value: the value at which the exponential decay stops. When ``decay_rate
      < 1``, ``end_value`` is treated as a lower bound, otherwise as an upper
      bound. Has no effect when ``decay_rate = 0``.

  Returns:
    schedule
      A function that maps step counts to values
  """
  schedules = [
      linear_schedule(
          init_value=init_value,
          end_value=peak_value,
          transition_steps=warmup_steps,
      ),
      exponential_decay(
          init_value=peak_value,
          transition_steps=transition_steps,
          decay_rate=decay_rate,
          transition_begin=transition_begin,
          staircase=staircase,
          end_value=end_value,
      ),
  ]
  return _join.join_schedules(schedules, [warmup_steps])

