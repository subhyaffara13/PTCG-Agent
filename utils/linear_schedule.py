
def linear_schedule(
    init_value: jax.typing.ArrayLike,
    end_value: jax.typing.ArrayLike,
    transition_steps: int,
    transition_begin: int = 0,
) -> base.Schedule:
  r"""Schedule with linear transition from ``init_value`` to ``end_value``.

  More precisely, the learning rate at iteration :math:`t` is given by:

  .. math::
    \begin{cases}
      I, & \text{if } t < B \\
      I + \frac{t - B}{T} (E - I), & \text{if } B \leq t < B + T \\
      E, & \text{if } t \geq B + T
    \end{cases}

  where :math:`I` is the initial value, :math:`E` is the end value,
  :math:`B` is the transition begin, and :math:`T` is the transition steps.

  This schedule is equivalent to :func:`optax.polynomial_schedule` with
  ``power=1``.

  Args:
    init_value: initial value for the scalar to be annealed.
    end_value: end value of the scalar to be annealed.
    transition_steps: number of steps over which annealing takes place. The
      scalar starts changing at ``transition_begin`` steps and completes the
      transition by ``transition_begin + transition_steps`` steps. If
      ``transition_steps <= 0``, then the entire annealing process is disabled
      and the value is held fixed at ``init_value``.
    transition_begin: must be positive. After how many steps to start annealing
      (before this many steps the scalar value is held fixed at ``init_value``).

  Returns:
    schedule
      A function that maps step counts to values.

  Examples:
    >>> schedule_fn = optax.linear_schedule(
    ...    init_value=1.0, end_value=0.01, transition_steps=100)
    >>> schedule_fn(0)  # learning rate on the first iteration
    Array(1., dtype=float32, weak_type=True)
    >>> schedule_fn(100)  # learning rate on the last iteration
    Array(0.01, dtype=float32, weak_type=True)
  """
  return polynomial_schedule(
      init_value=init_value,
      end_value=end_value,
      power=1,
      transition_steps=transition_steps,
      transition_begin=transition_begin,
  )


def linear_schedule(start_e: float,
                    end_e: float,
                    duration: int) -> Callable[[int], float]:
  slope = (end_e - start_e) / duration

  @jax.jit
  def _call(t: int) -> float:
    return max(slope * t + start_e, end_e)

  return _call


def linear_schedule(start_e: float,
                    end_e: float,
                    duration: int) -> Callable[[int], float]:
  slope = (end_e - start_e) / duration

  def _call(t: int) -> float:
    return max(slope * t + start_e, end_e)

  return _call

