
def _compress(self: Array, condition: ArrayLike,
              axis: int | None = None, *, out: None = None,
              size: int | None = None, fill_value: ArrayLike = 0) -> Array:
  """Return selected slices of this array along given axis.

  Refer to :func:`jax.numpy.compress` for full documentation.
  """
  return lax_numpy.compress(condition, self, axis=axis, out=out,
                            size=size, fill_value=fill_value)

