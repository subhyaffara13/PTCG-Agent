
def scale_gradient(
    inputs: base.ArrayTree, scale: jax.typing.ArrayLike) -> base.ArrayTree:
  """Scales gradients for the backwards pass.

  Args:
    inputs: A nested array.
    scale: The scale factor for the gradient on the backwards pass.

  Returns:
    An array of the same structure as `inputs`, with scaled backward gradient.
  """
  # Special case scales of 1. and 0. for more efficiency.
  if scale == 1.0:
    return inputs
  if scale == 0.0:
    return jax.lax.stop_gradient(inputs)
  return _scale_gradient(inputs, scale)

