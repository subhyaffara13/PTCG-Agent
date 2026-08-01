
def avg_pool(
  inputs, window_shape, strides=None, padding='VALID', count_include_pad=True
):
  """Pools the input by taking the average over a window.

  Args:
    inputs: input data with dimensions (batch, window dims..., features).
    window_shape: a shape tuple defining the window to reduce over.
    strides: a sequence of ``n`` integers, representing the inter-window
      strides (default: ``(1, ..., 1)``).
    padding: either the string ``'SAME'``, the string ``'VALID'``, or a sequence
      of ``n`` ``(low, high)`` integer pairs that give the padding to apply before
      and after each spatial dimension (default: ``'VALID'``).
    count_include_pad: a boolean whether to include padded tokens
      in the average calculation (default: ``True``).
  Returns:
    The average for each window slice.
  """
  y = pool(inputs, 0.0, lax.add, window_shape, strides, padding)
  if count_include_pad:
    y = y / np.prod(window_shape)
  else:
    div_shape = inputs.shape[:-1] + (1,)
    if len(div_shape) - 2 == len(window_shape):
      div_shape = (1,) + div_shape[1:]
    y = y / pool(
      jnp.ones(div_shape), 0.0, lax.add, window_shape, strides, padding
    )
  return y

