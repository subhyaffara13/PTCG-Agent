
def _calc_P_Q(A: Array) -> tuple[Array, Array, Array]:
  if A.ndim != 2 or A.shape[0] != A.shape[1]:
    raise ValueError('expected A to be a square matrix')
  A_L1 = jnp_linalg.norm(A,1)
  n_squarings: Array
  U: Array
  V: Array
  if A.dtype == 'float64' or A.dtype == 'complex128':
   maxnorm = 5.371920351148152
   n_squarings = jnp.maximum(0, jnp.floor(jnp.log2(A_L1 / maxnorm)))
   A = A / 2 ** n_squarings.astype(A.dtype)
   conds = jnp.array([1.495585217958292e-002, 2.539398330063230e-001,
                      9.504178996162932e-001, 2.097847961257068e+000],
                      dtype=A_L1.dtype)
   idx = jnp.digitize(A_L1, conds)
   U, V = lax.switch(idx, [_pade3, _pade5, _pade7, _pade9, _pade13], A)
  elif A.dtype == 'float32' or A.dtype == 'complex64':
    maxnorm = 3.925724783138660
    n_squarings = jnp.maximum(0, jnp.floor(jnp.log2(A_L1 / maxnorm)))
    A = A / 2 ** n_squarings.astype(A.dtype)
    conds = jnp.array([4.258730016922831e-001, 1.880152677804762e+000],
                      dtype=A_L1.dtype)
    idx = jnp.digitize(A_L1, conds)
    U, V = lax.switch(idx, [_pade3, _pade5, _pade7], A)
  else:
    raise TypeError(f"A.dtype={A.dtype} is not supported.")
  P = U + V  # p_m(A) : numerator
  Q = -U + V # q_m(A) : denominator
  return P, Q, n_squarings

