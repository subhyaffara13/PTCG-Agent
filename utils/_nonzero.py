
def _nonzero(self: Array, *, fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None,
             size: int | None = None) -> tuple[Array, ...]:
  """Return indices of nonzero elements of an array.

  Refer to :func:`jax.numpy.nonzero` for the full documentation.
  """
  return lax_numpy.nonzero(self, size=size, fill_value=fill_value)

