
def _pade3(A: Array) -> tuple[Array, Array]:
  b = (120., 60., 12., 1.)
  M, N = A.shape
  ident = jnp.eye(M, N, dtype=A.dtype)
  A2 = _precise_dot(A, A)
  U = _precise_dot(A, (b[3]*A2 + b[1]*ident))
  V: Array = b[2]*A2 + b[0]*ident
  return U, V

