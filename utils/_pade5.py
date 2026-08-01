
def _pade5(A: Array) -> tuple[Array, Array]:
  b = (30240., 15120., 3360., 420., 30., 1.)
  M, N = A.shape
  ident = jnp.eye(M, N, dtype=A.dtype)
  A2 = _precise_dot(A, A)
  A4 = _precise_dot(A2, A2)
  U = _precise_dot(A, b[5]*A4 + b[3]*A2 + b[1]*ident)
  V: Array = b[4]*A4 + b[2]*A2 + b[0]*ident
  return U, V

