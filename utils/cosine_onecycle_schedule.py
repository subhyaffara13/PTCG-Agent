
def cosine_onecycle_schedule(
    transition_steps: int,
    peak_value: jax.typing.ArrayLike,  # float
    pct_start: float = 0.3,
    div_factor: float = 25.0,
    final_div_factor: float = 1e4,
) -> base.Schedule:
  """Returns a function which implements the onecycle learning rate schedule.

  This schedule increases the learning rate and then decreases it in a
  cosine-like manner. The number of steps over which the learning rate increases
  is determined by the ``pct_start`` argument. The maximum value of the learning
  rate is determined by the ``peak_value`` argument, the initial value of the
  learning rate is determined through the formula ``init_value = peak_value /
  div_factor``, and the final value is determined by the ``final_div_factor``
  argument.

  Args:
    transition_steps: Number of steps over which annealing takes place.
    peak_value: Maximum value attained by schedule at pct_start percent of the
      cycle (in number of steps).
    pct_start: The percentage of the cycle (in number of steps) spent increasing
      the learning rate.
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
      'cosine',
      peak_value / div_factor,
      {
          int(pct_start * transition_steps): div_factor,
          int(transition_steps): 1.0 / (div_factor * final_div_factor),
      },
  )

