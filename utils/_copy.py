
def _copy(self: list[int]):
    out: list[int] = []
    for elem in self:
        out.append(elem)
    return out


def _copy(self: Array) -> Array:
  """Return a copy of the array.

  Refer to :func:`jax.numpy.copy` for the full documentation.
  """
  return lax_numpy.copy(self)

