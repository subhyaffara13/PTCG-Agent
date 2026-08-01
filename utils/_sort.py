
def _sort(self: Array, axis: int | None = -1, *, kind: None = None,
          order: None = None, stable: bool = True, descending: bool = False) -> Array:
  """Return a sorted copy of an array.

  Refer to :func:`jax.numpy.sort` for full documentation.
  """
  return lax_numpy.sort(self, axis=axis, kind=kind, order=order,
                        stable=stable, descending=descending)

