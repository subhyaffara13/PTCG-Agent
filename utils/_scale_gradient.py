
def _scale_gradient(
    inputs: base.ArrayTree, scale: jax.typing.ArrayLike) -> base.ArrayTree:
  """Internal gradient scaling implementation."""
  del scale  # Only used for the backward pass defined in _scale_gradient_bwd.
  return inputs

