
def weighted_logsoftmax(
    x: jax.typing.ArrayLike, weights: jax.typing.ArrayLike) -> jax.Array:
  r"""Weighted logsoftmax.

  Computes
  .. math::
    (w_i \log(\exp x_i /(\sum_i \exp x_i )) )_{i=1}^n

  for :math:`x` the input ``x``, :math:`w` the ``weights``.
  For :math:`w_i = 0`, :math:`x_i=-\infty`, this implementation ensures that the
  output is 0 and not nan at the ith entry following the convention that
  :math:`0 \log 0 = 0`.

  Args:
    x: input array.
    weights: weights.

  Returns:
    logsoftmax of x multiplied elementwise by weights
  """
  logsoftmax_x = jax.nn.log_softmax(x, axis=-1)
  return jnp.where(
      weights != 0.0, weights * logsoftmax_x, jnp.zeros_like(logsoftmax_x)
  )

