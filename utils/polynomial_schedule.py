import logging

def polynomial_schedule(
    init_value: jax.typing.ArrayLike,
    end_value: jax.typing.ArrayLike,
    power: jax.typing.ArrayLike,
    transition_steps: int,
    transition_begin: int = 0,
) -> base.Schedule:
  r"""Constructs a schedule with polynomial transition from init to end value.

  This function transitions the learning rate from an initial value
  (``init_value``) to a final value (``end_value``) over a specified number of
  steps (``transition_steps``) with a polynomial function of power ``power``.
  The transition can optionally begin after a specified number of initial steps
  (``transition_begin``).

  More precisely, the learning rate at iteration :math:`t` is given by:

  .. math::
    \begin{cases}
      I, & \text{if } t < B \\
      (I - E) \left( 1 - \frac{t - B}{T} \right)^{P} + E, &
        \text{if } B \leq t < B + T \\
      E, & \text{if } t \geq B + T
    \end{cases}

  where :math:`I` is the initial value, :math:`E` is the end value,
  :math:`B` is the transition begin, :math:`T` is the transition steps,
  and :math:`P` is the power used for the polynomial transition.

  Args:
    init_value: initial value for the scalar to be annealed.
    end_value: end value of the scalar to be annealed.
    power: the power of the polynomial used to transition from init to end.
    transition_steps: number of steps over which annealing takes place.
      The scalar starts changing at ``transition_begin`` steps and completes
      the transition by ``transition_begin + transition_steps`` steps.
      If ``transition_steps <= 0``, then the entire annealing process is
      disabled and the value is held fixed at ``init_value``.
    transition_begin: must be positive. After how many steps to start annealing
      (before this many steps the scalar value is held fixed at ``init_value``).

  Returns:
    schedule
      A function that maps step counts to values.

  Examples:
    >>> schedule_fn = optax.polynomial_schedule(
    ...    init_value=1.0, end_value=0.01, transition_steps=100, power=2)
    >>> schedule_fn(0)  # learning rate on the first iteration
    Array(1., dtype=float32, weak_type=True)
    >>> schedule_fn(100)  # learning rate on the last iteration
    Array(0.01, dtype=float32, weak_type=True)

    The following example uses a non-zero ``transition_begin``. In this case
    the learning rate is kept constant for the first ``transition_begin``
    iterations:

    >>> schedule_fn = optax.polynomial_schedule(
    ...    init_value=1.0,
    ...    end_value=0.01,
    ...    transition_steps=100,
    ...    transition_begin=5,
    ...    power=2,
    ... )
    >>> counts = [0, 5, 6, 104, 105, 110]
    >>> print(
    ...    *[f'count:{i} value:{schedule_fn(i):.4f}' for i in counts],
    ...    sep='\n')
    count:0 value:1.0000
    count:5 value:1.0000
    count:6 value:0.9803
    count:104 value:0.0101
    count:105 value:0.0100
    count:110 value:0.0100
  """
  if transition_steps <= 0:
    logging.info(
        'A polynomial schedule was set with a non-positive `transition_steps` '
        'value; this results in a constant schedule with value `init_value`.'
    )
    return lambda count: init_value

  if transition_begin < 0:
    logging.info(
        'A polynomial schedule was set with a negative `transition_begin` '
        'value; this will result in `transition_begin` falling back to `0`.'
    )
    transition_begin = 0

  def schedule(count):
    count = jnp.clip(count - transition_begin, 0, transition_steps)
    frac = 1 - count / transition_steps
    return (init_value - end_value) * (frac**power) + end_value

  return schedule

