
def _cumprod(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
             out: None = None) -> Array:
  """Return the cumulative product of the array.

  Refer to :func:`jax.numpy.cumprod` for the full documentation.
  """
  return reductions.cumprod(self, axis=axis, dtype=dtype, out=out)

