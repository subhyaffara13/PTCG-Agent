
def exponential_decay(
    init_value: jax.typing.ArrayLike,
    transition_steps: int,
    decay_rate: float,
    transition_begin: int = 0,
    staircase: bool = False,
    end_value: Optional[jax.typing.ArrayLike] = None,
) -> base.Schedule:
  """Constructs a schedule with either continuous or discrete exponential decay.

  This function applies an exponential decay function to a provided initial
  value. When ``count >= transition_begin`` the function returns the decayed
  value as:

  .. code-block::

    rate_factor = ((count - transition_begin) / transition_steps)
    decayed_value = init_value * (decay_rate ** rate_factor)

  If the argument ``staircase`` is ``True`` then ``count / transition_steps`` is
  an integer division and the decayed value follows a staircase function.

  Args:
    init_value: the initial learning rate.
    transition_steps: must be positive. See the decay computation above.
    decay_rate: must not be zero. The decay rate.
    transition_begin: must be positive. After how many steps to start annealing
      (before this many steps the scalar value is held fixed at `init_value`).
    staircase: if ``True``, decay the values at discrete intervals.
    end_value: the value at which the exponential decay stops. When ``decay_rate
      < 1``, ``end_value`` is treated as a lower bound, otherwise as an upper
      bound. Has no effect when ``decay_rate = 0``.

  Returns:
    schedule
      A function that maps step counts to values.
  """

  if transition_steps <= 0:
    logging.info(
        'An exponential schedule was set with a non-positive `transition_steps`'
        ' value; this will result in a constant schedule with value '
        '`init_value`.'
    )
    return lambda count: init_value

  if decay_rate == 0:
    logging.info(
        'An exponential schedule was set with a zero `decay_rate` value; '
        'this will result in a constant schedule with value `init_value`.'
    )
    return lambda count: init_value

  if transition_begin < 0:
    logging.info(
        'An exponential schedule was set with a negative `transition_begin` '
        'value; this will result in `transition_begin` falling back to `0`.'
    )
    transition_begin = 0

  if end_value is not None:
    clip_fn = jnp.maximum if decay_rate < 1.0 else jnp.minimum

  def schedule(count):
    decreased_count = count - transition_begin
    p = decreased_count / transition_steps
    if staircase:
      p = jnp.floor(p)
    decayed_value = jnp.where(
        decreased_count <= 0, init_value, init_value * jnp.power(decay_rate, p)
    )
    if end_value is not None:
      decayed_value = clip_fn(decayed_value, end_value)  # pylint: disable=undefined-variable
    return decayed_value

  return schedule


def exponential_decay(step_size, decay_steps, decay_rate):
  def schedule(i):
    return step_size * decay_rate ** (i / decay_steps)
  return schedule

