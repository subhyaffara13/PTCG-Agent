
def cosine_decay_schedule(
    init_value: jax.typing.ArrayLike,
    decay_steps: int,
    alpha: jax.typing.ArrayLike = 0.0,
    exponent: jax.typing.ArrayLike = 1.0,
) -> base.Schedule:
  r"""Returns a function which implements cosine learning rate decay.

  This schedule smoothly decreases the learning rate over a specified number of
  steps (``decay_steps``). The decay follows a cosine function, with an optional
  exponent to modify the decay curve. A minimum value (``alpha``) ensures the
  learning rate does not drop entirely to zero.

  More precisely, the learning rate at iteration :math:`t` is given by:

  .. math::
    \begin{cases}
      \alpha I + (1 - \alpha) I  \left[ \frac{1}{2} \left( 1+ \cos \left( \pi\,\frac{t}{T} \right) \right) \right] ^p  & \text{, if } t \leq T \\
      \alpha I  & \text{, if } t > T
    \end{cases}

  where :math:`T` is the number of decay steps (``decay_steps``), :math:`p` is
  the ``exponent`` and :math:`I` is the initial value (``init_value``).

  Args:
    init_value: An initial value for the learning rate.
    decay_steps: Positive integer - the number of steps for which to apply
      the decay for.
    alpha: The minimum value of the multiplier used to adjust the
      learning rate. Defaults to 0.0.
    exponent:  The default decay is ``0.5 * (1 + cos(pi * t/T))``, where
      ``t`` is the current timestep and ``T`` is the ``decay_steps``. The
      exponent modifies this to be ``(0.5 * (1 + cos(pi * t/T))) ** exponent``.
      Defaults to 1.0.

  Returns:
    schedule
      A function that maps step counts to values.

  References:
    Loshchilov et al., `SGDR: Stochastic Gradient Descent with Warm Restarts
    <https://arxiv.org/abs/1608.03983>`_, 2017
  """  # noqa: E501
  if not decay_steps > 0:
    raise ValueError(
        'The cosine_decay_schedule requires positive decay_steps, got'
        f' {decay_steps=}.'
    )

  def schedule(count):
    # Avoid int -> int32 overflow in jitted code.
    nonlocal decay_steps
    decay_steps, count = jax.tree.map(
        lambda x: float(x) if isinstance(x, int) else x, (decay_steps, count)
    )

    count = jnp.minimum(count, decay_steps)
    cosine_decay = 0.5 * (1 + jnp.cos(jnp.pi * count / decay_steps))
    decayed = (1 - alpha) * cosine_decay**exponent + alpha
    return init_value * decayed

  return schedule

