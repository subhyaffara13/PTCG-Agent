
def max_pool(inputs, window_shape, strides=None, padding='VALID'):
  """Pools the input by taking the maximum of a window slice.

  Args:
    inputs: input data with dimensions (batch, window dims..., features).
    window_shape: a shape tuple defining the window to reduce over.
    strides: a sequence of ``n`` integers, representing the inter-window
      strides (default: ``(1, ..., 1)``).
    padding: either the string ``'SAME'``, the string ``'VALID'``, or a sequence
      of ``n`` ``(low, high)`` integer pairs that give the padding to apply before
      and after each spatial dimension (default: ``'VALID'``).
  Returns:
    The maximum for each window slice.
  """
  y = pool(inputs, -jnp.inf, lax.max, window_shape, strides, padding)
  return y

