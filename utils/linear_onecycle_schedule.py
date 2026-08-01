
def linear_onecycle_schedule(
    transition_steps: int,
    peak_value: jax.typing.ArrayLike,  # float
    pct_start: float = 0.3,
    pct_final: float = 0.85,
    div_factor: float = 25.0,
    final_div_factor: float = 1e4,
) -> base.Schedule:
  r"""Returns a learning rate with three linear phases.

  * *Phase 1*, from iteration 0 to ``pct_start * transition_steps``. The
    learning rate increases linearly from ``peak_value / div_factor`` to
    ``peak_value``.
  * *Phase 2*, from iteration ``pct_start * transition_steps`` to
    ``pct_final * transition_steps``. The learning rate decreases linearly from
    ``peak_value`` back to the initial ``peak_value/div_factor``.
  * *Phase 3*: For the remaining steps, the learning rate interpolates between
    ``peak_value/div_factor`` and ``peak_value / final_div_factor``. If
    ``final_div_factor`` is larger than ``div_factor``, this is a decreasing
    phase.

  Args:
    transition_steps: Number of steps over which annealing takes place.
    peak_value: Maximum value attained by schedule at pct_start percent of the
      cycle (in number of steps).
    pct_start: The percentage of the cycle (in number of steps) spent increasing
      the learning rate.
    pct_final: The percentage of the cycle (in number of steps) spent increasing
      to ``peak_value`` then decreasing back to ``init_value``.
    div_factor: Determines the initial value via ``init_value = peak_value /
      div_factor``.
    final_div_factor: Determines the final value via ``final_value = init_value
      / final_div_factor``.

  Returns:
    schedule
      A function that maps step counts to values

  References:
    Smith et al, `Super-Convergence: Very Fast Training of Neural Networks Using
    Large Learning Rates <https://arxiv.org/abs/1708.07120>`_, 2017
  """
  if transition_steps <= 0:
    raise ValueError(
        'A linear onecycle schedule was set with a non-positive '
        '`transition_steps`'
    )

  return piecewise_interpolate_schedule(
      'linear',
      peak_value / div_factor,
      {
          int(pct_start * transition_steps): div_factor,
          int(pct_final * transition_steps): 1.0 / div_factor,
          transition_steps: 1.0 / final_div_factor,
      },
  )

