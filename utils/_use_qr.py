
def _use_qr(u, m, n, params):
  """QDWH iteration using QR decomposition.

  Args:
  u: a matrix, with static (padded) shape M x N.
  m, n: the dynamic shape of the matrix, where m <= M and n <= N.
  params: the QDWH parameters.
  """
  a_minus_e_by_sqrt_c, sqrt_c, e = params
  M, N = u.shape

  y = _dynamic_concat(sqrt_c * u, jnp.eye(N, dtype=dtypes.dtype(u)), m)
  q, _ = lax_linalg.qr(y, full_matrices=False)
  # q1 = q[:m, :]
  q1 = _mask(lax.slice(q, (0, 0), (M, N)), (m, n))
  # q2 = (q[m:, :]).T.conj()
  q2 = lax.dynamic_slice_in_dim(q, m, N, axis=0)
  q2 = _mask(q2, (n, n)).T.conj()
  return e * u + a_minus_e_by_sqrt_c * (q1 @ q2)

