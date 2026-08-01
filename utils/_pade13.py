
def _pade13(A: Array) -> tuple[Array, Array]:
  b = (64764752532480000., 32382376266240000., 7771770303897600.,
       1187353796428800., 129060195264000., 10559470521600., 670442572800.,
       33522128640., 1323241920., 40840800., 960960., 16380., 182., 1.)
  M, N = A.shape
  ident = jnp.eye(M, N, dtype=A.dtype)
  A2 = _precise_dot(A, A)
  A4 = _precise_dot(A2, A2)
  A6 = _precise_dot(A4, A2)
  U = _precise_dot(A, _precise_dot(A6, b[13]*A6 + b[11]*A4 + b[9]*A2) + b[7]*A6 + b[5]*A4 + b[3]*A2 + b[1]*ident)
  V = _precise_dot(A6, b[12]*A6 + b[10]*A4 + b[8]*A2) + b[6]*A6 + b[4]*A4 + b[2]*A2 + b[0]*ident
  return U,V

