
def _dot(self: Array, b: ArrayLike, *, precision: lax.PrecisionLike = None,
         preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the dot product of two arrays.

  Refer to :func:`jax.numpy.dot` for the full documentation.
  """
  return tensor_contractions.dot(self, b, precision=precision, preferred_element_type=preferred_element_type)


def _dot(v1, v2):
    return (v1 * v2.conjugate()).real

