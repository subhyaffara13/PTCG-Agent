
def _argsort(self: Array, axis: int | None = -1, *, kind: None = None, order: None = None,
             stable: bool = True, descending: bool = False) -> Array:
  """Return the indices that sort the array.

  Refer to :func:`jax.numpy.argsort` for the full documentation.
  """
  return lax_numpy.argsort(self, axis=axis, kind=kind, order=order,
                           stable=stable, descending=descending)

