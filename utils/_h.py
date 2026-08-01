
def _H(x: Array) -> Array:
  return _T(x).conj()


def _H(x: ArrayLike) -> Array:
  return ufuncs.conjugate(jnp.matrix_transpose(x))

