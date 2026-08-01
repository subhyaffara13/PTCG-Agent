
def min_pool(inputs, window_shape, strides=None, padding='VALID'):
  """Pools the input by taking the minimum of a window slice.

  Args:
    inputs: Input data with dimensions (batch, window dims..., features).
    window_shape: A shape tuple defining the window to reduce over.
    strides: A sequence of ``n`` integers, representing the inter-window strides
      (default: ``(1, ..., 1)``).
    padding: Either the string ``'SAME'``, the string ``'VALID'``, or a sequence of
      ``n`` ``(low, high)`` integer pairs that give the padding to apply before and
      after each spatial dimension (default: ``'VALID'``).

  Returns:
    The minimum for each window slice.
  """
  return pool(inputs, jnp.inf, lax.min, window_shape, strides, padding)

