
def _cumsum(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
            out: None = None) -> Array:
  """Return the cumulative sum of the array.

  Refer to :func:`jax.numpy.cumsum` for the full documentation.
  """
  return reductions.cumsum(self, axis=axis, dtype=dtype, out=out)

