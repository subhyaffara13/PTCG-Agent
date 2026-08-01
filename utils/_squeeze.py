
def _squeeze(self: Array, axis: reductions.Axis = None) -> Array:
  """Remove one or more length-1 axes from array.

  Refer to :func:`jax.numpy.squeeze` for full documentation.
  """
  return lax_numpy.squeeze(self, axis=axis)


def _squeeze(a: Array, axis: tuple[int, ...]) -> Array:
  if axis is None:
    a_shape = np.shape(a)
    if not core.is_constant_shape(a_shape):
      # We do not even know the rank of the output if the input shape is not known
      raise ValueError("jnp.squeeze with axis=None is not supported with shape polymorphism")
    axis = tuple(i for i, d in enumerate(a_shape) if d == 1)
  return lax.squeeze(a, axis)

